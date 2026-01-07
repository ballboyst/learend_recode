<?php
  $val = isset($_REQUEST['param']) ? $_REQUEST['param'] : null;
  // $val=@$_REQUEST['param'];
  if(! isset($val)){
    die("NO PARAMETER");
  }
?>
<!DOCTYPE html>
<html>
    <head>
    <meta charset="UTF-8">
    </head>
    <body>
    <?php
    #echo "Input parameter:{$val}";
    ?>
    </body>
    </html>