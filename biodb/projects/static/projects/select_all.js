$(function() {
  $(".select-all").click(function() {
    if (this.checked)
      $(".robject").prop("checked", true);
    else
      $(".robject").prop("checked", false);
  })
})
