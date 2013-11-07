 namespace StitchPattern\Model;

 class StitchPattern
 {
     public $id;
     public $title;

     public function exchangeArray($data)
     {
         $this->id     = (!empty($data['id'])) ? $data['id'] : null;
         $this->title  = (!empty($data['title'])) ? $data['title'] : null;
     }
 }
