<?php
 return array(
     'controllers' => array(
         'invokables' => array(
             'StitchPattern\Controller\StitchPattern' => 'StitchPattern\Controller\StitchPatternController',
         ),
     ),
     'router' => array(
         'routes' => array(
             'stitchpattern' => array(
                 'type'    => 'segment',
                 'options' => array(
                     'route'    => '/stitchpattern[/][:action][/:id]',
                     'constraints' => array(
                         'action' => '[a-zA-Z][a-zA-Z0-9_-]*',
                         'id'     => '[0-9]+',
                     ),
                     'defaults' => array(
                         'controller' => 'StitchPattern\Controller\StitchPattern',
                         'action'     => 'index',
                     ),
                 ),
             ),
         ),
     ),
     'view_manager' => array(
         'template_path_stack' => array(
             'stitchpattern' => __DIR__ . '/../view',
         ),
     ),
 );
