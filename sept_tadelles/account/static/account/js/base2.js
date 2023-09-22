function openNavbar() {
	document.querySelector(".navbar").style.right = "0";
	document.querySelector(".navbar__openbtn").style.right = "-400px";
}

function closeNavbar() {
	document.querySelector(".navbar").style.right = "-400px";
	document.querySelector(".navbar__openbtn").style.right = "0";
}

document.addEventListener("DOMContentLoaded", function() {
	document.querySelector(".navbar__openbtn").addEventListener("click", openNavbar);
	document.querySelector(".navbar__closebtn").addEventListener("click", closeNavbar);
});