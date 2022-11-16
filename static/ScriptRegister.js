function change_avatar(to) {
  let inp_avatar = document.getElementById("id_avatar");
  
  inp_avatar.value = to;

  change_avatar_icon(to);
}

function change_value_avatar() {
  let inp_avatar = document.getElementById("id_avatar");
  let to = inp_avatar.value;
  change_avatar_icon(to);
}

function change_avatar_icon(to) {
  let avatar = document.getElementsByClassName("avatar");

  for (let i = 0; i < avatar.length; i++) {
    const element = avatar[i];
    if (i == to - 1) {
      element.style.background = "black";
    } else {
      element.style.background = "#1f1f1f";
    }
  }
}

document
  .getElementById("id_avatar")
  .addEventListener("click", change_value_avatar);
