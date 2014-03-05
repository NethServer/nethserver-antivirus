<?php

echo "<div class='dashboard-item'>";
echo $view->header()->setAttribute('template',$T('antivirus_title'));
echo "<dl>";
echo "<dt>".$T('status_label')."</dt><dd><span class='";
if ($view['alarm']) {
    echo "antivirus-red'>".$T('warning_label');
} else {
    echo "antivirus-green'>".$T('ok_label');
}
echo "</span></dd>";
echo "<dt>".$T('timestamp_label')."</dt><dd>"; echo $view->textLabel('timestamp'); "</dd>";
echo "</dl>";
echo "</div>";

$view->includeCSS("
  span.antivirus-green {
      padding: 3px;
      color: green;
      font-weight: bold;
  }
  span.antivirus-red {
      padding: 3px;
      color: red;
      font-weight: bold;
  }

");

