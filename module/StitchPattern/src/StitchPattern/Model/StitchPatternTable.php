<?php
 namespace StitchPattern\Model;

 use Zend\Db\TableGateway\TableGateway;
 use Zend\Db\Sql\Select;

 class StitchPatternTable
 {
     protected $tableGateway;

     public function __construct(TableGateway $tableGateway)
     {
         $this->tableGateway = $tableGateway;
     }

     public function fetchAll($id)
     {
         $resultSet = $this->tableGateway->select(array('user_id' => $id));
         return $resultSet;
     }

     public function fetchPublic($id = false)
     {
     	 if($id)
	         $resultSet = $this->tableGateway->select("user_id != $id and shared = 1");
		 else 
	         $resultSet = $this->tableGateway->select(array('shared' => true));

         return $resultSet;
     }

     public function getStitchPattern($id)
     {
         $id  = (int) $id;
         $rowset = $this->tableGateway->select(array('id' => $id));
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
             'preview'  => $stitchpattern->preview,
             'stitches'  => $stitchpattern->stitches,
             'user_id'  => $user_id,
             'shared'  => $stitchpattern->shared
         );

         $id = (int) $stitchpattern->id;
         if ($id == 0) {
             $this->tableGateway->insert($data);
         } else {
             if ($this->getStitchPattern($id)) {
                 $this->tableGateway->update($data, array('id' => $id));
             } else {
                 throw new \Exception('StitchPattern id does not exist');
             }
         }
     }

     public function deleteStitchPattern($id)
     {
         $this->tableGateway->delete(array('id' => (int) $id));
     }
 }
