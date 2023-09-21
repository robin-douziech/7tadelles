function openNavbar() {
	document.querySelector(".navbar").style.left = "0";
	document.querySelector(".navbar__openbtn").style.left = "-400px";
}

function closeNavbar() {
	document.querySelector(".navbar").style.left = "-400px";
	document.querySelector(".navbar__openbtn").style.left = "0";
}

document.addEventListener("DOMContentLoaded", function() {
	document.querySelector(".navbar__openbtn").addEventListener("click", openNavbar);
	document.querySelector(".navbar__closebtn").addEventListener("click", closeNavbar);
});