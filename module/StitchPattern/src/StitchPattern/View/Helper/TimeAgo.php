<?php

/**
 * Extension of the Coolcsn Zend Framework 2 Authorization Module
 *
 */

namespace StitchPattern\View\Helper;

use Zend\View\Helper\AbstractHelper;

class TimeAgo extends AbstractHelper {

	public function __construct() {	}

	function getTime($date) {

		if (empty($date)) {
			return "No date provided";
		}

		$periods = array("s", "m", "h", "day", "week", "month", "yr", "decade");
		$lengths = array("60", "60", "24", "7", "4.35", "12", "10");
		$now = time();
		$unix_date = strtotime($date);

		// check validity of date
		if (empty($unix_date)) {
			return "Bad date";
		}

		// is it future date or past date
		if ($now > $unix_date) {
			$difference = $now - $unix_date;
			$tense = "ago";
		} else {
			$difference = $unix_date - $now;
			$tense = "from now";
		}
		
		if($difference < 86400) {
			for ($j = 0; $difference >= $lengths[$j] && $j < count($lengths) - 1; $j++) {
				$difference /= $lengths[$j];
			}
	
			$difference = round($difference);
			/* add an 's' on the end
			if ($difference != 1) {
				$periods[$j] .= "s";
			}*/
	
			return "$difference$periods[$j] {$tense}";
		} else if($difference < 31536000){
			return date('j M',$unix_date);
		} else {
			return date('M y',$unix_date);
		}
	}
}
