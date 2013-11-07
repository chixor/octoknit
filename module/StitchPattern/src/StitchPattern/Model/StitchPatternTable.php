 namespace StitchPattern\Model;

 use Zend\Db\TableGateway\TableGateway;

 class StitchPatternTable
 {
     protected $tableGateway;

     public function __construct(TableGateway $tableGateway)
     {
         $this->tableGateway = $tableGateway;
     }

     public function fetchAll()
     {
         $resultSet = $this->tableGateway->select();
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

     public function saveStitchPattern(StitchPattern $album)
     {
         $data = array(
             'artist' => $album->artist,
             'title'  => $album->title,
         );

         $id = (int) $album->id;
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
