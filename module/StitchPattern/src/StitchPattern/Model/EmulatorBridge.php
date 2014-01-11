<?php
namespace StitchPattern\Model;

class EmulatorBridge {
	protected $id;
	protected $dr;
	protected $path;
	protected $output;

	public function __construct() {
	}

	public function convert($id, $title, $stitches) {
		// determine the directory name
		$dirname = $id . '-' . $this -> sanitize($title, true, true);
		$path = 'data/files/';

		$this->id = $id;
		$this->dr = $dirname;
		$this->path = $path;
		$this->output = '/output.jpg';	

		// cleanup previous converting operations
		if (is_dir($path . $dirname))
			@rmdir($path . $dirname);

		// create the blank directory
		$this -> cpdir('emulator/img-blank', $path . $dirname);

		// convert the pattern into 1bit bitmap
		$this -> strToBmp($stitches, $path . $dirname);

		// insert pattern
		shell_exec('python emulator/insertpattern.py '. $path . $dirname .'/file-01.dat 901 '. $path . $dirname . $this->output .' '. $path . $dirname .'/file-01.dat');

		// check contents
		$result = shell_exec('python emulator/dumppattern.py '. $path . $dirname .'/file-01.dat 901');

		// split pattern to tandy floppy drive tracks
		shell_exec('cd '. $path . $dirname . ' && python ../../../emulator/splitfile2track.py ./file-01.dat 2>&1');

		return $result;
	}

	public function pddemulate($id, $title) {
		error_reporting(E_ALL);
		
		// determine the directory name
		$dirname = $id . '-' . $this -> sanitize($title, true, true);
		$path = 'data/files/';

		header("Content-type: text/plain");
		
		// tell php to automatically flush after every output
		// including lines of output produced by shell commands
		$this->disable_ob();
		
		echo "Using /$dirname/ with /dev/cu.usbserial-A4WYNI7I";
		echo "                                                                                                                                                                                                                                                                                                                                    \n";
		echo "                                                                                                                                                                                                                                                                                                                                    \n";
		echo "                                                                                                                                                                                                                                                                                                                                    \n";
												
		//$command = 'ping 127.0.0.1';
		$command = 'python -u emulator/PDDemulate.py '. $path . $dirname .'/ /dev/cu.usbserial-A4WYNI7I 2>&1';
		system($command);
	}
	
	public function disable_ob() {
	    // Turn off output buffering
	    ini_set('output_buffering', 'off');
	    // Turn off PHP output compression
	    ini_set('zlib.output_compression', false);
	    // Implicitly flush the buffer(s)
	    ini_set('implicit_flush', true);
	    ob_implicit_flush(true);
	    // Clear, and turn off output buffering
	    while (ob_get_level() > 0) {
	        // Get the curent level
	        $level = ob_get_level();
	        // End the buffering
	        ob_end_clean();
	        // If the current level has not changed, abort
	        if (ob_get_level() == $level) break;
	    }
	    // Disable apache output buffering/compression
	    if (function_exists('apache_setenv')) {
	        apache_setenv('no-gzip', '1');
	        apache_setenv('dont-vary', '1');
	    }
	}
	
	public function getImagePath() {
		$type = pathinfo($this->path . $this->dr . $this->output, PATHINFO_EXTENSION);
		$data = file_get_contents($this->path . $this->dr . $this->output);
		$base64 = 'data:image/' . $type . ';base64,' . base64_encode($data);
		
		return $base64;
	}

	public function strToBmp($str, $dir) {
		// Prepare the inputs and outputs
		$color_array = str_split($str);
		$img_width = 60;
		$img_height = 150;
		$im = imagecreatetruecolor($img_width, $img_height);
		$xpx = (int)0;
		$ypx = (int)0;

		// Initialise colours;
		$black = imagecolorallocate($im, 0, 0, 0);
		$white = imagecolorallocate($im, 255, 255, 255);

		// Iterate through and build the bmp
		foreach ($color_array as $y) {
			if ($y == 1) {
				imagesetpixel($im, $xpx, $ypx, $black);
			} else {
				imagesetpixel($im, $xpx, $ypx, $white);
			}

			$xpx++;
			// Don't need to "draw" a white pixel for 0. Just draw nothing and add to the counter.
			if ($xpx % 60 == 0) {
				$ypx++;
				$xpx = 0;
			}
		}

		imagejpeg($im, $dir . $this->output);
	}

	public function cpdir($src, $dst) {
		$dir = opendir($src);
		@mkdir($dst);
		while (false !== ($file = readdir($dir))) {
			if (($file != '.') && ($file != '..')) {
				if (is_dir($src . '/' . $file)) {
					recurse_copy($src . '/' . $file, $dst . '/' . $file);
				} else {
					copy($src . '/' . $file, $dst . '/' . $file);
				}
			}
		}
		closedir($dir);
	}

	/**
	 * Function: sanitize
	 * Returns a sanitized string, typically for URLs.
	 *
	 * Parameters:
	 *     $string - The string to sanitize.
	 *     $force_lowercase - Force the string to lowercase?
	 *     $anal - If set to *true*, will remove all non-alphanumeric characters.
	 */
	public function sanitize($string, $force_lowercase = true, $anal = false) {
		$strip = array("~", "`", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "=", "+", "[", "{", "]", "}", "\\", "|", ";", ":", "\"", "'", "&#8216;", "&#8217;", "&#8220;", "&#8221;", "&#8211;", "&#8212;", "â€”", "â€“", ",", "<", ".", ">", "/", "?");
		$clean = trim(str_replace($strip, "", strip_tags($string)));
		$clean = preg_replace('/\s+/', "-", $clean);
		$clean = ($anal) ? preg_replace("/[^a-zA-Z0-9]/", "", $clean) : $clean;
		return ($force_lowercase) ? (function_exists('mb_strtolower')) ? mb_strtolower($clean, 'UTF-8') : strtolower($clean) : $clean;
	}

}
