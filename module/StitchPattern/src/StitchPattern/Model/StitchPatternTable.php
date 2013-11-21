<?php
 namespace StitchPattern\Model;

 use Zend\Db\TableGateway\TableGateway;

 class StitchPatternTable
 {
     protected $tableGateway;

     public function __construct(TableGateway $tableGateway)
     {
         $this->tableGateway = $tableGateway;
     }

     public function fetchAll($id)
     {
         $resultSet = $this->tableGateway->select(function (\Zend\Db\Sql\Select $select) use ($id) {
         	$select->join('user','stitchpattern.user_id = user.id', array('username'))->where("user.id = $id")->order('title');
         });
         return $resultSet;
     }

     public function fetchPublic($id = false)
     {
     	 if($id)
	         $resultSet = $this->tableGateway->select(function (\Zend\Db\Sql\Select $select) use ($id) {
	         	$select->join('user','stitchpattern.user_id = user.id', array('username'))->where("user.id != $id and shared = 1")->order('title');
	         });
		 else 
	         $resultSet = $this->tableGateway->select(function (\Zend\Db\Sql\Select $select) {
	         	$select->join('user','stitchpattern.user_id = user.id', array('username'))->where("shared = 1")->order('title');
	         });

         return $resultSet;
     }

     public function fetchPublicFromUser($id)
     {
         $resultSet = $this->tableGateway->select(function (\Zend\Db\Sql\Select $select) use ($id) {
         	$select->join('user','stitchpattern.user_id = user.id', array('username'))->where("user.id = $id and shared = 1")->order('title');
         });

         return $resultSet;
     }

     public function getStitchPattern($id)
     {
         $id  = (int) $id;
         $rowset = $this->tableGateway->select(function (\Zend\Db\Sql\Select $select) use ($id) {
         	$select->join('user','stitchpattern.user_id = user.id', array('username'))->where("stitchpattern.id = $id");
         });
         $row = $rowset->current();
         if (!$row) {
             throw new \Exception("Could not find row $id");
         }
         return $row;
     }

     public function saveStitchPattern(StitchPattern $stitchpattern, $user_id)
     {
         $data = array(
             'title'  => $stitchpattern->title,
             'stitches'  => $stitchpattern->stitches,
             'user_id'  => $user_id,
             'shared'  => $stitchpattern->shared
         );

         $id = (int) $stitchpattern->id;
         if ($id == 0) {
             $this->tableGateway->insert($data);
			 $stitchpattern->setId($this->tableGateway->lastInsertValue);
         } else {
             if ($this->getStitchPattern($id)) {
                 $this->tableGateway->update($data, array('id' => $id));
             } else {
                 throw new \Exception('StitchPattern id does not exist');
             }
         }
		 return $stitchpattern;
     }

     public function deleteStitchPattern($id)
     {
         $this->tableGateway->delete(array('id' => (int) $id));
     }
 }
