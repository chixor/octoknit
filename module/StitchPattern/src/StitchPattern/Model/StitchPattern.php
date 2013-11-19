<?php
 namespace StitchPattern\Model;

 use Zend\InputFilter\InputFilter;
 use Zend\InputFilter\InputFilterAwareInterface;
 use Zend\InputFilter\InputFilterInterface;

 class StitchPattern implements InputFilterAwareInterface
 {
     public $id;
     public $title;
     public $preview;
     public $previewDir;
	 public $stitches;
	 public $shared;
     protected $inputFilter;

     public function exchangeArray($data)
     {
         $this->id     = (!empty($data['id'])) ? $data['id'] : null;
         $this->title  = (!empty($data['title'])) ? $data['title'] : null;
         $this->preview  = (!empty($data['preview'])) ? $data['preview'] : null;
         $this->stitches  = (!empty($data['stitches'])) ? $data['stitches'] : null;
         $this->user_id  = (!empty($data['user_id'])) ? $data['user_id'] : null;
         $this->shared  = (!empty($data['shared'])) ? $data['shared'] : 0;

		// prepare for file storage / retrieval, remove "data:image/png;base64,"
		$this->preview = substr($this->preview, strpos($this->preview,",")+1);
		$this->previewDir = $this->getPreviewImageDir($this);
     }
	 
	 public function setId($id)
	 {
	 	$this->id = $id;
		$this->previewDir = $this->getPreviewImageDir($this);
	 }

     public function getArrayCopy()
     {
         return get_object_vars($this);
     }

     public function setInputFilter(InputFilterInterface $inputFilter)
     {
         throw new \Exception("Not used");
     }

     public function getInputFilter()
     {
         if (!$this->inputFilter) {
             $inputFilter = new InputFilter();

             $inputFilter->add(array(
                 'name'     => 'id',
                 'required' => true,
                 'filters'  => array(
                     array('name' => 'Int'),
                 ),
             ));

             $inputFilter->add(array(
                 'name'     => 'shared',
                 'required' => true,
                 'filters'  => array(
                     array('name' => 'Int'),
                 ),
             ));

             $inputFilter->add(array(
                 'name'     => 'title',
                 'required' => true,
                 'filters'  => array(
                     array('name' => 'StripTags'),
                     array('name' => 'StringTrim'),
                 ),
                 'validators' => array(
                     array(
                         'name'    => 'StringLength',
                         'options' => array(
                             'encoding' => 'UTF-8',
                             'min'      => 1,
                             'max'      => 100,
                         ),
                     ),
                 ),
             ));

             $inputFilter->add(array(
                 'name'     => 'preview',
                 'required' => true,
                 'filters'  => array(
                     array('name' => 'StripTags'),
                     array('name' => 'StringTrim'),
                 )
             ));

             $inputFilter->add(array(
                 'name'     => 'stitches',
                 'required' => true,
                 'filters'  => array(
                     array('name' => 'StripTags'),
                     array('name' => 'StringTrim'),
                 )
             ));

             $this->inputFilter = $inputFilter;
         }

         return $this->inputFilter;
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

	public function getPreviewImageDir(StitchPattern $stitchpattern) {
		return 'data/previews/' . $stitchpattern->id . '-' . $this -> sanitize($stitchpattern->title, true, true) . '.png';
	}
	
	public function savePreview() {
		file_put_contents($this->previewDir, base64_decode($this->preview));
	}
	
	public function deletePreview() {
		@unlink($this->previewDir);
	}
 }
