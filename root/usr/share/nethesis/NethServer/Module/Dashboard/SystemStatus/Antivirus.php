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
        $fh = $this->getPhpWrapper()->fopen("/var/log/clamav/freshclam-updates.log", "r");
        if(is_resource($fh)) {
            list($status, $timestamp) = $this->getPhpWrapper()->fscanf($fh, "%s %s");
            $this->getPhpWrapper()->fclose($fh);
        } else {
            $status = '';
            $timestamp = '';
        }

        $max = 0;
        $fileList = glob('/var/lib/clamav/*.{cvd,cld}', GLOB_BRACE);
        foreach ($fileList as $file) {
            $changeTime = filemtime($file);
            if ($changeTime > $max) {
                $max = $changeTime;
            }
        }

        $staleSignatures = time() - $max > 3600 * 24 * 5;
        $runningUpdates = time() - intval(strtotime($timestamp)) < 3600 * 12;

        if ($runningUpdates && $staleSignatures && $status === 'error') {
            $this->alarm = TRUE;
        }

        $this->timestamp = $timestamp;       
    }
 
    public function process()
    {
        $this->readAntivirus();
    }
 
    public function prepareView(\Nethgui\View\ViewInterface $view)
    {
        if (!$this->timestamp) {
            $this->readAntivirus();
        }

        $view['timestamp'] = $this->timestamp;
        $view['alarm'] = $this->alarm;
    }
}
