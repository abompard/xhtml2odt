#!/usr/bin/php
<?php
# vim: set expandtab tabstop=4 shiftwidth=4:
/**
 * xhtml2odt - XHTML to ODT XML transformation
 * 
 * This script can convert a wiki page to the OpenDocument Text (ODT) format,
 * standardized as ISO/IEC 26300:2006, and the native format of office suites
 * such as OpenOffice.org, KOffice, and others.
 * 
 * It uses a template ODT file which will be filled with the converted
 * content of the exported Wiki page.
 * 
 * Based on the work on {@link http://open.comsultia.com/docbook2odf/
 * docbook2odt}, by Roman Fordinal
 * 
 * @author Aurélien Bompard <aurelien@bompard.org>
 * @copyright Aurélien Bompard <aurelien@bompard.org> 2009-2010
 * @license http://www.gnu.org/licenses/agpl-3.0.html AGPLv3
 * 
 * Licensed under the AGPL version 3.0.
 * A copy of this license is available in LICENSE file or at
 * http://www.gnu.org/licenses/agpl-3.0.html
 *
 * @package xhtml2odt
 */


/**
 * Conversion failure
 */
class OdfException extends Exception {}


/**
 * Handling of an ODT file based on a template (another ODT file)
 */
class dcODF {
    protected $odtfile;
    protected $odtfilepath;
    protected $tmpfiles = array();
    protected $contentXml;
    protected $stylesXml;
    protected $autostyles = array();
    protected $styles = array();
    protected $fonts = array();
    protected $images = array();
    public $template;
    public $xslparams = array();
    public $get_remote_images = true;
    const PIXEL_TO_CM = 0.026458333;

    public function __construct($template) {
        $this->template = $template;
        if (! class_exists('ZipArchive')) {
            throw new OdfException('Zip extension not loaded - check your php
                settings, PHP5.2 minimum with zip extension is required for
                using OdtExport'); ;
        }
        // Loading content.xml and styles.xml from the template
        $this->odtfile = new ZipArchive();
        if ($this->odtfile->open($template) !== true) {
          throw new OdfException("Error while Opening the file '$template' -
                                  Check your odt file");
        }
        if (($this->contentXml = $this->odtfile->getFromName('content.xml')) === false) {
            throw new OdfException("Nothing to parse - check that the
                                    content.xml file is correctly formed");
        }
        if (($this->stylesXml = $this->odtfile->getFromName('styles.xml')) === false) {
          throw new OdfException("Nothing to parse - check that the
                                  styles.xml file is correctly formed");
        }
        $this->odtfile->close();
        // Use you app's cache directory here instead of null:
        $tmp = tempnam(null, md5(uniqid()));
        copy($template, $tmp);
        $this->odtfilepath = $tmp;
    }

    public function __destruct() {
        if (file_exists($this->odtfilepath)) {
            unlink($this->odtfilepath);
        }
        foreach ($this->tmpfiles as $tmp) {
            unlink($tmp);
        }
    }

    public function __toString() {
        return $this->contentXml;
    }

    /**
     * Main function which runs the other
     *
     * If your app has a templating engine, you may want to use the template
     * ODT file as one of you app's templates. You would then do the following
     * steps:
     * - run it here through your template engine, which would produce a mix
     *   of ODT XML and XHTML.
     * - pass the result to the {@link xhtml2odt} method, which would only
     *   convert the XHTML to ODT, and leave the ODT untouched
     * - the rest of the function is identical
     */
    public function compile() {
        global $html, $replace_tag;
        //$html = YourAppsTemplatingEngine($this->template);
        // here we'll just use the global $html variable.
        $odt = $this->xhtml2odt($html);
        $odt = str_replace('<'.'?xml version="1.0" encoding="utf-8"?'.'>', '', $odt);
        //print $html;
        //print $this->contentXml;
        //print $odt;
        //print "\n";
        //exit();
        // If you're using the ODT file as a template in a templating engine,
        // you can just set $this->contentXml to the output of xhtml2odt()
        if ($replace_tag and strpos($this->contentXml, $replace_tag) !== false) {
            $this->contentXml = preg_replace("/<text:p[^>]*>$replace_tag<\/text:p>/", $odt, $this->contentXml);
        } else {
            $this->contentXml = str_replace("</office:text>", "$odt</office:text>", $this->contentXml);
        }
        $this->addStyles();
    }

    /**
     * Clean up the HTML we get in input
     *
     * Because the stylesheets will only accept well-formed (and if possible
     * valid) XHTML.
     *
     * If you have XHTML *and* ODT mixed up in input, because you used
     * the ODT file as a template in your templating engine, then you
     * *can't* run it through "tidy". Or else you'd have to use the
     * input-xml option, and it does strange things like removing the
     * white space after links. I didn't find a way around this.
     */
    public function cleanupInput($xhtml) {
        // add namespace if you used the ODT file as a template
        //$xhtml = str_replace("<office:document-content", '<office:document-content xmlns="http://www.w3.org/1999/xhtml"', $xhtml);

        /* Won't work if you have ODT XML *and* XHTML as input */
        if (extension_loaded('tidy')) {
            $tidy_config = array(
                    'output-xhtml' => true,
                    'add-xml-decl' => false,
                    'indent' => false,
                    'tidy-mark' => false,
                    //'input-encoding' => "latin1",
                    'output-encoding' => "utf8",
                    'doctype' => "auto",
                    'wrap' => 0,
                    'char-encoding' => "utf8",
                ); 
            $tidy = new tidy;
            $tidy->parseString($xhtml, $tidy_config, 'utf8');
            $tidy->cleanRepair();
            //$xhtml = "$tidy";
        }

        // replace html codes with unicode
        // http://www.mail-archive.com/analog-help@lists.meer.net/msg03670.html
        //$xhtml = str_replace("&nbsp;","&#160;",$xhtml);
        $xhtml = html_entity_decode($xhtml, ENT_COMPAT, "UTF-8");

        return $xhtml;
    }

    /**
     * Convert from XHTML to ODT using the stylesheets
     *
     * @param string $xhtml XHTML to convert
     * @return string resulting ODT XML
     */
    public function xhtml2odt($xhtml) {
        global $url;
        $xhtml = self::cleanupInput($xhtml);
        // handle images
        $xhtml = preg_replace('#<img ([^>]*)src="http://'.$url.'#', '<img \1src="', $xhtml);
        $xhtml = preg_replace_callback('#<img [^>]*src="(/[^"]+)"#', array($this,"handleLocalImg"), $xhtml);
        if ($this->get_remote_images) {
            $xhtml = preg_replace_callback('#<img [^>]*src="(https?://[^"]+)"#', array($this,"handleRemoteImg"), $xhtml);
        }
        // run the stylesheets
        $xsl = dirname(__FILE__)."/xsl";
        $xmldoc = new DOMDocument();
        $xmldoc->loadXML($xhtml); 
        $xsldoc = new DOMDocument();
        $xsldoc->load($xsl."/xhtml2odt.xsl");
        $proc = new XSLTProcessor();
        $proc->importStylesheet($xsldoc);
        foreach ($this->xslparams as $pkey=>$pval) {
            $proc->setParameter("", $pkey, $pval);
        }
        $proc->setParameter("", "debug", "1");
        $output = $proc->transformToXML($xmldoc);
        if ($output === false) {
            throw new OdfException('XSLT transformation failed');
        }
        return $output;
    }

    /**
     * Handling of local images (on this server)
     *
     * Must be called as a regexp callback. Outsources all the hard work to
     * the {@link handleImg} method.
     *
     * @param array $matches regexp matches
     * @return string regexp replacement
     */
    protected function handleLocalImg($matches) {
        /* If you're a web app, you can do this:
        $file = $_SERVER["DOCUMENT_ROOT"].$matches[1];
        return $this->handleImg($file, $matches);
        */
        // We're a command-line app, so...
        global $url;
        $matches[1] = $url."/".$matches[1];
        return $this->handleRemoteImg($matches);
    }

    /*
     * Download remote images with cURL
     *
     * Must be called as a regexp callback. Outsources all the hard work to
     * the {@link handleImg} method.
     *
     * @param array $matches regexp matches
     * @return string regexp replacement
     */
    protected function handleRemoteImg($matches) {
        $url = $matches[1];
        // Use you app's cache directory here instead of null:
        $tempfilename = tempnam(null,"xhtml2odt-");
        $this->tmpfiles []= $tempfilename;
        $tempfile = fopen($tempfilename,"w");
        if ($tempfile === false) {
            return $matches[0];
        }
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $url);
        curl_setopt($ch, CURLOPT_FILE, $tempfile);
        curl_setopt($ch, CURLOPT_BINARYTRANSFER, true);
        $result = curl_exec($ch);
        if ($result === false) {
            return $matches[0];
        }
        curl_close($ch);
        fclose($tempfile);
        return $this->handleImg($tempfilename, $matches);
    }

    /**
     * Insertion of the image in the ODT file and the content.xml file
     *
     * @param string $file the path to the image
     * @param array $matches regexp matches
     * @return string regext replacement
     */
    protected function handleImg($file, $matches) {
        $size = @getimagesize($file);
        if ($size === false) {
            $size = array($this->xslparams["img_default_width"],
                          $this->xslparams["img_default_height"]);
        }
        list ($width, $height) = $size;
        $width *= self::PIXEL_TO_CM;
        $height *= self::PIXEL_TO_CM;
        $this->importImage($file);
        return str_replace($matches[1],"Pictures/".basename($file).'" width="'.$width.'cm" height="'.$height.'cm', $matches[0]);
    }
        
    /**
     * Adds an image to the list of files to import
     *
     * The image must be added to content.xml by another means (see {@link
     * handleImg})
     *
     * @param string $filename path to the image
     * @throws OdfException
     */
    public function importImage($filename) {
        if (!is_readable($filename)) {
            throw new OdfException("Image is not readable or does not exist");
        }
        $this->images[$filename] = basename($filename);
    }

    /**
     * Inserts the generated ODT XML code into the content.xml and styles.xml
     * files
     */
    protected function _parse() {
        // automatic styles
        if ($this->autostyles) {
            $autostyles = implode("\n",$this->autostyles);
            if (strpos($this->contentXml, '<office:automatic-styles/>') !== false) {
                $this->contentXml = str_replace('<office:automatic-styles/>',
                                        '<office:automatic-styles>'.$autostyles.'</office:automatic-styles>',
                                        $this->contentXml);
            } else {
                $this->contentXml = str_replace('</office:automatic-styles>',
                                        $autostyles.'</office:automatic-styles>', $this->contentXml);
            }
        }
        // regular styles
        if ($this->styles) {
            $styles = implode("\n",$this->styles);
            $this->stylesXml = str_replace('</office:styles>',
                                   $styles.'</office:styles>', $this->stylesXml);
        }
        // fonts
        if ($this->fonts) {
            $fonts = implode("\n",$this->fonts);
            $this->contentXml = str_replace('</office:font-face-decls>',
                                    $fonts.'</office:font-face-decls>', $this->contentXml);
        }
    }

    /**
     * Internal save
     *
     * @throws OdfException
     */
    protected function _save() {
        $this->odtfile->open($this->odtfilepath, ZIPARCHIVE::CREATE);
        $this->_parse();
        if (! $this->odtfile->addFromString('content.xml', $this->contentXml)) {
            throw new OdfException('Error during file export');
        }
        if (! $this->odtfile->addFromString('styles.xml', $this->stylesXml)) {
            throw new OdfException('Error during file export');
        }
        foreach ($this->images as $imageKey => $imageValue) {
            $this->odtfile->addFile($imageKey, 'Pictures/' . $imageValue);
        }
        $this->odtfile->close();
    }

    /**
     * Exports the file as an HTTP attachment.
     *
     * If you're a web app, you'll probably want this.
     *
     * @param string $name name of the file to download (optional)
     * @throws OdfException
     */
    public function exportAsAttachedFile($name="") {
        $this->_save();
        if (headers_sent($filename, $linenum)) {
            throw new OdfException("headers already sent ($filename at $linenum)");
        }
        if( $name == "" ) {
            $name = md5(uniqid()) . ".odt";
        }
        header('Content-type: application/vnd.oasis.opendocument.text');
        header('Content-Disposition: attachment; filename="'.$name.'"');
        readfile($this->odtfilepath);
    }

    /**
     * Saves the file to the disk
     *
     * Mainly useful for the command-line app, see {@link
     * exportAsAttachedFile} to have the browser download the file.
     *
     * @param string $name path to the file on the disk
     * @throws OdfException
     */
    public function saveToFile($name="") {
        $this->_save();
        if( $name == "" ) {
            $name = md5(uniqid()) . ".odt";
        }
        copy($this->odtfilepath, $name);
    }

    /**
     * Adds all missing styles and fonts in the document
     */
    protected function addStyles() {
        $xsl = dirname(__FILE__)."/xsl";
        $contentxml = new DOMDocument();
        $contentxml->loadXML($this->contentXml); 
        $stylesxml = new DOMDocument();
        $stylesxml->loadXML($this->stylesXml); 
        $xsldoc = new DOMDocument();
        $xsldoc->load($xsl."/styles.xsl");
        $proc = new XSLTProcessor();
        $proc->importStylesheet($xsldoc);
        $this->contentXml = $proc->transformToXML($contentxml);
        $this->stylesXml = $proc->transformToXML($stylesxml);
        if ($this->contentXml === false or $this->stylesXml === false) {
            throw new OdfException('Adding of styles failed');
        }
    }

}


function parseOpts() {
    $shortopts = "i:o:t:";
    $longopts = array(
        "url:",
        "no-network",
        "replace:",
        "top-header-level:",
        "img-default-width:",
        "img-default-height:",
    );
    $usage = sprintf("Usage: %s [options] -i input.html -o output.odt -t template.odt\n", $GLOBALS["argv"][0]);
    $options = getopt($shortopts, $longopts);
    foreach (array("i", "o", "t") as $reqopt) {
        if (!array_key_exists($reqopt, $options)) {
            die("Missing '-$reqopt' option.\n".$usage);
        }
    }
    return $options;
}

/**
 * Main function, everything starts here
 */
function main() {
    global $html, $url, $replace_tag;

    $options = parseOpts();
    $html_file = $options["i"];
    $tpl_file = $options["t"];
    $url = array_key_exists("url", $options) ? $options["url"] : "";
    $top_header_level = array_key_exists("top-header-level", $options)
                            ? int($options["top-header-level"]) : 1;
    $img_width = array_key_exists("img-default-width", $options) 
                            ? $options["img-default-width"] : "8cm";
    $img_height = array_key_exists("img-default-height", $options) 
                            ? $options["img-default-height"] : "6cm";
    $replace_tag = array_key_exists("replace", $options)
                            ? $options["replace"] : "";

    $html = file_get_contents($html_file);

    $odf = new dcOdf($tpl_file);

    $odf->xslparams["url"] = $url; // this would be your app's URL
    // the following setting depends on how <h> tags are used in you app
    $odf->xslparams["heading_minus_level"] = $top_header_level;
    // set the following values from your config
    $odf->get_remote_images = array_key_exists("no-network", $options);
    $odf->xslparams["img_default_width"] = $img_width;
    $odf->xslparams["img_default_height"] = $img_height;

    $odf->compile();

    $odf->saveToFile($options["o"]);
    print "Wrote document to: ".$options["o"]."\n";
}

main();

?>
