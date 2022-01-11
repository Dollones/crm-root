function show_or_hide(el_id) {
  var x = document.getElementById(el_id);
  var i = document.getElementById("icon")
  if (x.type === "password") {
    x.type = "text";
    i.innerHTML = i.innerHTML.replace("visibility_off","visibility");
  } else {
    x.type = "password";
    i.innerHTML = i.innerHTML.replace("visibility","visibility_off");
  }
}

function show_or_hide2(el_id) {
  var x = document.getElementById(el_id);
  var i = document.getElementById("icon2")
  if (x.type === "password") {
    x.type = "text";
    i.innerHTML = i.innerHTML.replace("visibility_off","visibility");
  } else {
    x.type = "password";
    i.innerHTML = i.innerHTML.replace("visibility","visibility_off");
  }
}

function show_or_hide3(el_id) {
  var x = document.getElementById(el_id);
  var i = document.getElementById("icon3")
  if (x.type === "password") {
    x.type = "text";
    i.innerHTML = i.innerHTML.replace("visibility_off","visibility");
  } else {
    x.type = "password";
    i.innerHTML = i.innerHTML.replace("visibility","visibility_off");
  }
}