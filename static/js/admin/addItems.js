
let mainContainer = document.querySelector('.addItems');
let addButton = document.querySelector('#btnAdd');

function addRow() {
	let div = document.createElement('div');
	div.className = '';
	div.innerHTML = `
		<div class="form-group form-row">
		    <label for="item_name" class="col-12 col-sm-3 col-form-label">Item Name:</label>
	        <input type="text" name="item_name" id="item_name" class="form-control col-12 col-sm-9" required="">
        </div>
        <div class="form-group form-row">
		    <label for="qty" class="col-12 col-sm-3 col-form-label">Quantity:</label>
			<input type="number" name="qty" id="qty" class="form-control col-12 col-sm-9" required="">
        </div>
        <div class="form-group form-row">
		    <label for="unit_price" class="col-12 col-sm-3 col-form-label">Unit Price:</label>
			<input type="number" name="unit_price" id="unit_price" class="form-control col-12 col-sm-9" required="">
        </div>
        <div class="container-fluid">
        	<label for="" class="col-12 col-sm-3 col-form-label">Remove above column</label>
			<input type="button" value="-" class="btn btn-danger float-right" onclick="removeRow(this)" />
		</div>
	`;
		
	mainContainer.appendChild(div);
}

function removeRow(input) {
  mainContainer.removeChild(input.parentNode.parentNode);
}

addButton.addEventListener('click', addRow);