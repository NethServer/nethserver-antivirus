<?php
namespace NethServer\Module\Dashboard\SystemStatus;

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

/**
 * Retrieve antivirus db update status
 *
 * @author Giacomo Sanchietti
 */
class Antivirus extends \Nethgui\Controller\AbstractController
{

    public $sortId = 80;
 
    private $timestamp = '';
    private $alarm = FALSE;

    private function readAntivirus()
    {
        $max = 0;
        $fileList = glob('/var/lib/clamav/*.{cvd,cld,ndb,hdb,cdb}', GLOB_BRACE);
        foreach ($fileList as $file) {
            $changeTime = filemtime($file);
            if ($changeTime > $max) {
                $max = $changeTime;
            }
        }

        $now = time();
        $staleSignatures = $now - $max > 3600 * 24 * 3;
        if ($staleSignatures) {
            $this->alarm = TRUE;
        }

        $this->timestamp = min($max, $now);
    }
 
 
    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        $this->readAntivirus();
        $view['timestamp'] = strftime("%F %R", $this->timestamp);
        $view['alarm'] = $this->alarm;
    }
}
