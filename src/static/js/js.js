function redirectToPath(path) {
  window.location.href = path;
}

function getData(selectChange) {
  selectChange.addEventListener("change", function (event) {
    const option = selectChange.options[selectChange.selectedIndex];
    const path = option.getAttribute("data-path");
    window.location.href = path;
  });
}
