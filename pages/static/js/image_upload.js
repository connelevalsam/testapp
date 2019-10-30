    let input   = document.querySelector('#image_uploads');
	let preview = document.querySelector('.preview');
	let label = document.querySelector('label');
	let list = document.createElement('ol');
			let listItem = document.createElement('li');
	input.style.opacity = 0;
	/*
	opacity is used to hide the file input instead of 'visibility: hidden' or 'display: none', because assistive technology interpretes the latter two styles to mean the file input isn't interactive.
	*/
	input.addEventListener('change', updateDisplay);
	label.addEventListener('mouseenter', changeLabel);
	label.addEventListener('mouseleave', restoreLabel);
	/*

	*/
	function updateDisplay() {
		// body...
		while(preview.firstChild) {
			preview.removeChild(preview.firstChild);
		}
		let paragraph = document.createElement('p');
		let cFiles = input.files;
		if (cFiles.length === 0) {
			paragraph.textContent = 'No files currently selected';
		} else {
			preview.appendChild(list);
			for(let i = 0; i < cFiles.length; i++) {
				let image = document.createElement('img');
				image.style.width  = '4em';
				image.style.height = '4em';
				image.style.contain;
				image.src = window.URL.createObjectURL(cFiles[i]);
				listItem.appendChild(image);
			}
			list.appendChild(listItem);
		}
	}

	function changeLabel() {
		label.style.cursor          = 'pointer';
		label.style.fontSize        = '20px';
		label.style.backgroundColor = '#eee';
	}

	function restoreLabel() {
		label.style.cursor          = 'default';
		label.style.fontSize        = '16px';
		label.style.backgroundColor = '#fff';
	}