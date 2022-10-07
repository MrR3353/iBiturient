// storing values in local storage
var subjects = [
	document.querySelector('#rus'),
	document.querySelector('#math'),
	document.querySelector('#phys'),
	document.querySelector('#chem'),
	document.querySelector('#hist'),
	document.querySelector('#soc'),
	document.querySelector('#inf'),
	document.querySelector('#bio'),
	document.querySelector('#geo'),
	document.querySelector('#lang'),
	document.querySelector('#litr'),
	document.querySelector('#extra')
]

//var radiobtns = [
//    document.querySelector('#paid'),
//    document.querySelector('#budget')
//]

document.addEventListener('DOMContentLoaded', function() {
	subjects.forEach(function(item, i, arr) {
		if (item) {
			item.value = localStorage.getItem(item.id) || "";
		}
		item.addEventListener('input', function() {
        	localStorage.setItem(item.id, this.value);
    	});
	});



//	radiobtns.forEach(function(item, i, arr) {
//	    if (item) {
////			item.checked = localStorage.getItem(item.id);
//            document.getElementById(item.id).checked = localStorage.getItem(item.id);
//            alert(item.id);
//            alert(localStorage.getItem(document.getElementById(item.id).checked));
//		}
//		item.addEventListener('change', function() {
////		    alert(item.id);
//		    localStorage.setItem(item.id, this.checked);
//		    if (item.id == 'paid') {
//		        localStorage.setItem('budget', false)
//		    } else {
//		        localStorage.setItem('paid', false)
//		    }
//    	});
//
//	});
});

var clear = document.querySelector('#clear');
clear.onclick = function() {
    subjects.forEach(function(item, i, arr) {
        item.value = "";
        localStorage.setItem(item.id, "");
	});
}

