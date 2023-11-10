$(document).ready( function () {
    $('#t_author').DataTable(
    {"lengthMenu" : [2,3,5,10,20],
lengthChange: true,
info: true,
pageLength: 2

}
);
} );