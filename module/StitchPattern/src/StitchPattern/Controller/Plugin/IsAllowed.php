<?php

/**
 * Extension of the Coolcsn Zend Framework 2 Authorization Module
 * 
 */

namespace StitchPattern\Controller\Plugin;

use Zend\Mvc\Controller\Plugin\AbstractPlugin;
use CsnAuthorization\Controller\Plugin;

class IsAllowed extends \CsnAuthorization\Controller\Plugin\IsAllowed {

    protected $auth;
    protected $acl;

    public function __construct($auth, $acl) {
        $this->auth = $auth;
        $this->acl = $acl;
    }

    /**
     * Checks whether the given user has acces to a resource.
	 * First invokes the parent for general ACL verification, then checks the instance specifically
     * 
     * @param StitchPattern $resource
     * @param User $identity
     * @param string $privilege
     */
    public function __invoke(\StitchPattern\Model\StitchPattern $resource, \CsnUser\Entity\User $identity, $privilege) {
    	$sharePrivilages = array('convert','upload','pddemulate');

		if(parent::__invoke('StitchPattern\Controller',$privilege)) {
			if($identity->getRole()->getName() == 'admin') return true;
			else if($resource->user_id == $identity->getId()) return true;
			else if(in_array($privilege, $sharePrivilages) && $resource->shared) return true;
		}
		return false;
    }
}
