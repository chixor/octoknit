<?php
/**
 * CsnUser Configuration
 *
 * If you have a ./config/autoload/ directory set up for your project, you can
 * drop this config file in it and change the values as you wish.
 */

/**
 * Static salt
 *
 * This constant value is prepended to the password before hashing
 *
 * Default value: 'aFGQ475SDsdfsaf2342'
 * Accepted values: Any string
 */
const STATIC_SALT = 'aFGQ475SDsdfsaf2342';

$settings = array(
    /**
     * Login Redirect Route
     *
     * Upon successful login the user will be redirected to the entered route
     *
     * Default value: 'user'
     * Accepted values: A valid route name within your application
     *
     */
    'login_redirect_route' => 'home',

    /**
     * Logout Redirect Route
     *
     * Upon logging out the user will be redirected to the enterd route
     *
     * Default value: 'user'
     * Accepted values: A valid route name within your application
     */
    'logout_redirect_route' => 'home',

    /**
     * Visibility of navigation menu
     *
     * If set to false the navigation menu does not appear
     *
     * Default value: true
     * Accepted values: true/false
     */
    'nav_menu' => false,
 
 /**
 * You do not need to edit below this line
 * ---------------------------------------
 */
    'static_salt' => STATIC_SALT,
);
return array(
    'csnuser' => $settings,
    'doctrine' => array(
        'authentication' => array(
            'orm_default' => array(
                'credential_callable' => function(CsnUser\Entity\User $user, $passwordGiven) {
					if ($user->getPassword() == md5(STATIC_SALT . $passwordGiven . $user->getPasswordSalt()) &&
						$user->getState() == 1) {
						return true;
					}
					else {
						return false;
					}
                },
            ),
        ),
    ),
);
