<?php
namespace NethServer\Module\Proxy;

/*
 * Copyright (C) 2013 Nethesis S.r.l.
 *
 * This script is part of NethServer.
 *
 * NethServer is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * NethServer is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with NethServer.  If not, see <http://www.gnu.org/licenses/>.
 */

use Nethgui\System\PlatformInterface as Validate;

/**
 * Configure antivirus behaviour
 *
 * @author Giacomo Sanchietti
 */
class Antivirus extends \Nethgui\Controller\AbstractController
{

    public $sortId = 30;
    
    // Declare all parameters
    public function initialize()
    {
        parent::initialize();

        $this->declareParameter('status', Validate::SERVICESTATUS, array(array('configuration', 'squidclamav', 'status'),array('configuration', 'c-icap', 'status')));
    }

    public function writeStatus($value)
    {
        return array($value,$value);
    }
    
    public function readStatus($v1, $v2)
    {
        return $v1;
    }


    protected function onParametersSaved($changes)
    {
        $this->getPlatform()->signalEvent('nethserver-squidclamav-update@post-process');
        $this->getPlatform()->signalEvent('nethserver-c-icap-update@post-process');
    }
}
