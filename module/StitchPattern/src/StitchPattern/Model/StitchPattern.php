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
 }
