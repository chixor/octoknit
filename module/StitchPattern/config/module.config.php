<?php
 return array(
     'controllers' => array(
         'invokables' => array(
             'StitchPattern\Controller' => 'StitchPattern\Controller\StitchPatternController',
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
                         'controller' => 'StitchPattern\Controller',
                         'action'     => 'index',
                     ),
                 ),
             ),
             'u' => array(
                 'type'    => 'segment',
                 'options' => array(
                     'route'    => '/u[/][/:username]',
                     'constraints' => array(
                         'username' => '[a-zA-Z_-][a-zA-Z0-9_-]*',
                     ),
                     'defaults' => array(
                         'controller' => 'StitchPattern\Controller',
                        'action'        => 'user',
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
    // extend the default ACL view helper to include stitch pattern level perms
    'view_helpers' => array(
        'factories' => array(
            'isAllowed' => function($sm) {
              $sm = $sm->getServiceLocator(); // $sm was the view helper's locator
              $auth = $sm->get('Zend\Authentication\AuthenticationService');
              $acl = $sm->get('acl');

              $helper = new \StitchPattern\View\Helper\IsAllowed($auth, $acl);
              return $helper;
            },
            'timeAgo' => function($sm) {
              $helper = new \StitchPattern\View\Helper\TimeAgo();
              return $helper;
            }
        ),
    ),
    // extend the default ACL controller plugin to include stitch pattern level perms
    'controller_plugins' => array(
        'factories' => array(
            'isAllowed' => function($sm) {
              $sm = $sm->getServiceLocator(); // $sm was the view helper's locator
              $auth = $sm->get('Zend\Authentication\AuthenticationService');
              $acl = $sm->get('acl');

              $plugin = new \StitchPattern\Controller\Plugin\IsAllowed($auth, $acl);
              return $plugin;
            }
        ),
    ),
 );
