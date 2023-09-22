function openNavbar() {
	document.querySelector(".navbar").style.right = "0";

	document.querySelector(".navbar__openbtnl1").style.backgroundColor = "#222";
	document.querySelector(".navbar__openbtnl2").style.transform = "translate(-50%, -50%) rotate(135deg)";
	document.querySelector(".navbar__openbtnl3").style.transform = "translate(-50%, -50%) rotate(45deg)";

	document.querySelector(".navbar__openbtn").removeEventListener("click", openNavbar);
	document.querySelector(".navbar__openbtn").addEventListener("click", closeNavbar);
	document.querySelector(".navbar__openbtn").removeEventListener("mouseenter", mouseEnterButton);
	document.querySelector(".navbar__openbtn").removeEventListener("mouseleave", mousLeaveButton);
}

function closeNavbar() {
	document.querySelector(".navbar").style.right = "-400px";

	document.querySelector(".navbar__openbtnl1").style.backgroundColor = "white";
	document.querySelector(".navbar__openbtnl2").style.transform = "translate(-50%, -50%) translate(0, -15px)";
	document.querySelector(".navbar__openbtnl3").style.transform = "translate(-50%, -50%) translate(0, 15px)";

	document.querySelector(".navbar__openbtn").removeEventListener("click", closeNavbar);
	document.querySelector(".navbar__openbtn").addEventListener("click", openNavbar);
	document.querySelector(".navbar__openbtn").addEventListener("mouseenter", mouseEnterButton);
	document.querySelector(".navbar__openbtn").addEventListener("mouseleave", mousLeaveButton);

}

function mouseEnterButton() {
	document.querySelector(".navbar__openbtnl2").style.left = "50%";
	document.querySelector(".navbar__openbtnl3").style.left = "50%";
}

function mousLeaveButton() {
	document.querySelector(".navbar__openbtnl2").style.left = "40%";
	document.querySelector(".navbar__openbtnl3").style.left = "60%";
}

document.addEventListener("DOMContentLoaded", function() {
	document.querySelector(".navbar__openbtn").addEventListener("click", openNavbar);
	document.querySelector(".navbar__openbtn").addEventListener("mouseenter", mouseEnterButton);
	document.querySelector(".navbar__openbtn").addEventListener("mouseleave", mousLeaveButton);
});