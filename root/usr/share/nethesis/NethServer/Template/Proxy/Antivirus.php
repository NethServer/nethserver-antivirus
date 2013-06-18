<?php

echo $view->fieldset()->setAttribute('template', $T('Antivirus_status'))
    ->insert($view->radioButton('status', 'enabled'))
    ->insert($view->radioButton('status', 'disabled'));

echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);
