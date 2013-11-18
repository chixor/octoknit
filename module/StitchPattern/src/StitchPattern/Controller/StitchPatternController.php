<?php
namespace StitchPattern\Controller;

use Zend\Mvc\Controller\AbstractActionController;
use Zend\View\Model\ViewModel;
use StitchPattern\Model\StitchPattern;
use StitchPattern\Model\USBCable;
use StitchPattern\Form\StitchPatternForm;

class StitchPatternController extends AbstractActionController {
	protected $stitchpatternTable;
	protected $usbcableTable;
	protected $emulatorbridge;

	public function indexAction() {
		$this->layout()->setVariable('pageTypeList', true);
		if($this->identity()) {
			$vm = new ViewModel( array(
				'mySP' => $this -> getStitchPatternTable() -> fetchAll($this -> identity() -> getId()),
				'sharedSP' => $this -> getStitchPatternTable() -> fetchPublic($this -> identity() -> getId())
			));
			$vm->setTemplate('stitch-pattern/stitch-pattern/list.phtml');
			return $vm;
		} else {
			return new ViewModel( array('stitchpatterns' => $this -> getStitchPatternTable() -> fetchPublic()));
		}
	}

	public function addAction() {
		$form = new StitchPatternForm();
		$form -> get('submit') -> setValue('Add');
		$form -> get('shared') -> setValue('0');

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$stitchpattern = new StitchPattern();
			$form -> setInputFilter($stitchpattern -> getInputFilter());
			$form -> setData($request -> getPost());

			if ($form -> isValid()) {
				$stitchpattern -> exchangeArray($form -> getData());
				$this -> getStitchPatternTable() -> saveStitchPattern($stitchpattern,$this->identity()->getId());
				$stitchpattern -> savePreview();

				// Redirect to list of stitchpatterns
				return $this -> redirect() -> toRoute('stitchpattern');
			}
		}
		return array('form' => $form);
	}

	public function editAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		$form = new StitchPatternForm();
		$form -> bind($stitchpattern);
		$form -> get('submit') -> setAttribute('value', 'Edit');

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$form -> setInputFilter($stitchpattern -> getInputFilter());
			$form -> setData($request -> getPost());

			if ($form -> isValid()) {
				$this -> getStitchPatternTable() -> saveStitchPattern($stitchpattern,$this->identity()->getId());
				$stitchpattern -> savePreview();

				// Redirect to list of stitchpatterns
				return $this -> redirect() -> toRoute('stitchpattern');
			}
		}

		return array('id' => $stitchpattern->id, 'form' => $form, );
	}

	public function shareAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		$stitchpattern->shared = !($stitchpattern->shared);
		$this -> getStitchPatternTable() -> saveStitchPattern($stitchpattern,$this->identity()->getId());
		return $this -> redirect() -> toRoute('stitchpattern', array('action' => 'index'));
	}

	public function deleteAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$del = $request -> getPost('del', 'No');

			if ($del == 'Yes') {
				$this -> getStitchPatternTable() -> deleteStitchPattern($stitchpattern->id);
			}

			// Redirect to list of stitchpatterns
			return $this -> redirect() -> toRoute('home');
		}

		return array('id' => $stitchpattern->id, 'stitchpattern' => $this -> getStitchPatternTable() -> getStitchPattern($stitchpattern->id));
	}

	public function convertAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		return array(
			'result' => $this -> getEmulatorBridge() -> convert($stitchpattern->id, $stitchpattern->title, $stitchpattern->stitches),
			'imageURL' => $this -> getEmulatorBridge() -> getImagePath(),
			'id' => $stitchpattern->id
		);
	}

	public function uploadAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		$hasCablePluggedIn = false;
		$cables = $this -> getUSBCableTable() -> fetchAll();

		foreach($cables as $key=>$value) {
			if (shell_exec('ls '.$value->id) != null)
				$hasCablePluggedIn = true;
		}

		return array(
			'usbCable' => $hasCablePluggedIn,
			'id' => $stitchpattern->id
		);
	}
	
	public function pddemulateAction() {
		$stitchpattern = $this->getStitchPatternFromRouteACL();

		$this -> getEmulatorBridge() -> pddemulate($stitchpattern->id, $stitchpattern->title);

		return $this->response;
	}

	// Get the StitchPattern with the specified id.  An exception is thrown
	// if it cannot be found, in which case go to the index page.
	// only return the stitchpattern object if this user has permission to perform this action on it
	public function getStitchPatternFromRouteACL() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern');
		}

		try {
			$stitchpattern = $this -> getStitchPatternTable() -> getStitchPattern($id);
		} catch (\Exception $ex) {
			return $this -> redirect() -> toRoute('stitchpattern', array('action' => 'index'));
		}

		// check if user has perms on this specific instance
		if($this->isAllowed($stitchpattern, $this->identity(), $this->params()->fromRoute('action', 0))) {
			return $stitchpattern;
		} else {
			return $this -> redirect() -> toRoute('stitchpattern', array('action' => 'index'));
		}
	}

	public function getStitchPatternTable() {
		if (!$this -> stitchpatternTable) {
			$sm = $this -> getServiceLocator();
			$this -> stitchpatternTable = $sm -> get('StitchPattern\Model\StitchPatternTable');
		}
		return $this -> stitchpatternTable;
	}

	public function getUSBCableTable() {
		if (!$this -> usbcableTable) {
			$sm = $this -> getServiceLocator();
			$this -> usbcableTable = $sm -> get('StitchPattern\Model\USBCableTable');
		}
		return $this -> usbcableTable;
	}

	public function getEmulatorBridge() {
		if (!$this -> emulatorbridge) {
			$sm = $this -> getServiceLocator();
			$this -> emulatorbridge = $sm -> get('StitchPattern\Model\EmulatorBridge');
		}
		return $this -> emulatorbridge;
	}
}
