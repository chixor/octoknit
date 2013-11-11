<?php
namespace StitchPattern\Controller;

use Zend\Mvc\Controller\AbstractActionController;
use Zend\View\Model\ViewModel;
use StitchPattern\Model\StitchPattern;
use StitchPattern\Form\StitchPatternForm;

class StitchPatternController extends AbstractActionController {
	protected $stitchpatternTable;
	protected $emulatorbridge;

	public function indexAction() {
		if ($this -> zfcUserAuthentication() -> hasIdentity()) {
			return new ViewModel( array('stitchpatterns' => $this -> getStitchPatternTable() -> fetchAll($this -> zfcUserAuthentication() -> getIdentity() -> getId())));
		} else {
			return new ViewModel( array('stitchpatterns' => $this -> getStitchPatternTable() -> fetchPublic()));
		}

	}

	public function addAction() {
		$form = new StitchPatternForm();
		$form -> get('submit') -> setValue('Add');

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$stitchpattern = new StitchPattern();
			$form -> setInputFilter($stitchpattern -> getInputFilter());
			$form -> setData($request -> getPost());

			if ($form -> isValid()) {
				$stitchpattern -> exchangeArray($form -> getData());
				$this -> getStitchPatternTable() -> saveStitchPattern($stitchpattern);

				// Redirect to list of stitchpatterns
				return $this -> redirect() -> toRoute('stitchpattern');
			}
		}
		return array('form' => $form);
	}

	public function editAction() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern', array('action' => 'add'));
		}

		// Get the StitchPattern with the specified id.  An exception is thrown
		// if it cannot be found, in which case go to the index page.
		try {
			$stitchpattern = $this -> getStitchPatternTable() -> getStitchPattern($id);
		} catch (\Exception $ex) {
			return $this -> redirect() -> toRoute('stitchpattern', array('action' => 'index'));
		}

		$form = new StitchPatternForm();
		$form -> bind($stitchpattern);
		$form -> get('submit') -> setAttribute('value', 'Edit');

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$form -> setInputFilter($stitchpattern -> getInputFilter());
			$form -> setData($request -> getPost());

			if ($form -> isValid()) {
				$this -> getStitchPatternTable() -> saveStitchPattern($stitchpattern);

				// Redirect to list of stitchpatterns
				return $this -> redirect() -> toRoute('stitchpattern');
			}
		}

		return array('id' => $id, 'form' => $form, );
	}

	public function deleteAction() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern');
		}

		$request = $this -> getRequest();
		if ($request -> isPost()) {
			$del = $request -> getPost('del', 'No');

			if ($del == 'Yes') {
				$id = (int)$request -> getPost('id');
				$this -> getStitchPatternTable() -> deleteStitchPattern($id);
			}

			// Redirect to list of stitchpatterns
			return $this -> redirect() -> toRoute('stitchpattern');
		}

		return array('id' => $id, 'stitchpattern' => $this -> getStitchPatternTable() -> getStitchPattern($id));
	}

	public function convertAction() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern');
		}
		$pattern = $this -> getStitchPatternTable() -> getStitchPattern($id);

		return array(
			'result' => $this -> getEmulatorBridge() -> convert($id, $pattern -> title, $pattern -> stitches),
			'imageURL' => $this -> getEmulatorBridge() -> getImagePath(),
			'id' => $id
		);
	}

	public function uploadAction() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern');
		}
		$pattern = $this -> getStitchPatternTable() -> getStitchPattern($id);

		if (shell_exec('ls /dev/cu.usbserial-A4WYNI7I') == null)
			$usbCable = false;
		else
			$usbCable = true;

		return array(
			'usbCable' => $usbCable,
			'id' => $id
		);
	}
	
	public function pddemulateAction() {
		$id = (int)$this -> params() -> fromRoute('id', 0);
		if (!$id) {
			return $this -> redirect() -> toRoute('stitchpattern');
		}
		$pattern = $this -> getStitchPatternTable() -> getStitchPattern($id);

		$this -> getEmulatorBridge() -> pddemulate($id, $pattern -> title);

		return $this->response;
	}

	public function getStitchPatternTable() {
		if (!$this -> stitchpatternTable) {
			$sm = $this -> getServiceLocator();
			$this -> stitchpatternTable = $sm -> get('StitchPattern\Model\StitchPatternTable');
		}
		return $this -> stitchpatternTable;
	}

	public function getEmulatorBridge() {
		if (!$this -> emulatorbridge) {
			$sm = $this -> getServiceLocator();
			$this -> emulatorbridge = $sm -> get('StitchPattern\Model\EmulatorBridge');
		}
		return $this -> emulatorbridge;
	}
}