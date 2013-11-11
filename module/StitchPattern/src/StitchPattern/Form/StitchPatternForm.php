<?php
 namespace StitchPattern\Form;

 use Zend\Form\Form;

 class StitchPatternForm extends Form
 {
     public function __construct($name = null)
     {
         // we want to ignore the name passed
         parent::__construct('stitchpattern');

         $this->add(array(
             'name' => 'id',
             'type' => 'Hidden',
         ));
         $this->add(array(
             'name' => 'stitches',
             'type' => 'Hidden',
         ));
         $this->add(array(
             'name' => 'preview',
             'type' => 'Hidden',
         ));
         $this->add(array(
             'name' => 'title',
             'type' => 'Text',
             'attributes' => array(
                 'placeholder' => 'Title',
                 'class' => 'form-control'
             ),
         ));
         $this->add(array(
             'name' => 'submit',
             'type' => 'Submit',
             'attributes' => array(
                 'value' => 'Go',
                 'class' => 'btn btn-primary',
                 'id' => 'submitbutton',
             ),
         ));
     }
 }
