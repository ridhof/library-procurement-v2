// Call the dataTables jQuery plugin
$(document).ready(function () {
  var table = $("#dataTable").DataTable({
    order: [[2, "desc"]],
  });

  table.column(2).visible(false);
});
