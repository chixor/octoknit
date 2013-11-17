<?php

/**
 * Extension of the Coolcsn Zend Framework 2 Authorization Module
 * 
 */

namespace StitchPattern\View\Helper;

use Zend\View\Helper\AbstractHelper;
use CsnAuthorization\View\Helper;

class IsAllowed extends \CsnAuthorization\View\Helper\IsAllowed {
    
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
    public function __invoke(\StitchPattern\Model\StitchPattern $resource, $identity, $privilege) {
    	$sharePrivilages = array('convert','upload','pddemulate');

		if(parent::__invoke('StitchPattern\Controller',$privilege)) {
			if($identity && $identity->getRole()->getName() == 'admin') return true;
			else if($identity && $resource->user_id == $identity->getId()) return true;
			else if(in_array($privilege, $sharePrivilages) && $resource->shared) return true;
		}
		return false;
    }

}
