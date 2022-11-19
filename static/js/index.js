window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		const prediction = document.getElementById('prediction'); 
		const output = document.getElementById('output');
		const oThr = document.getElementById('oThr')
		prediction.textContent = 'Procesando...';
		input = $('#imageinput')[0]
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			formData.append('thickness', output.textContent);
			formData.append('thr', oThr.textContent);
			console.log(output.textContent);
			$.ajax({
				url: "http://localhost:5000/processing", // fix this to your liking
				type:"POST",
				data: formData,
				cache: false,
				processData:false,
				contentType:false,
				error: function(data){
					console.log("upload error" , data);
					console.log(data.getAllResponseHeaders());
				},
				success: function(data){
					bytestring = data['status'];
					image = bytestring.split('\'')[1];
					imagebox.attr('src' , 'data:image/png;base64,'+image);
					imagebox.height(280);
					imagebox.width(280);
					console.log(data['text']);
					prediction.textContent = data['text'];
				}
			});
		}
	});
};

function onRangeChange(range){
	const output = document.getElementById('output');
	output.textContent = range.value;
}

function onThRangeChange(range){
	const output = document.getElementById('oThr');
	output.textContent = range.value;
}

function readUrl(input){
    imagebox = $('#imagebox')
    console.log("evoked readUrl")

    if(input.files && input.files[0]){
		let reader = new FileReader();
		reader.onload = function(e){
			console.log(e)
			
			imagebox.attr('src',e.target.result); 
			imagebox.height(e.height);
			imagebox.width(e.width);
		}
		reader.readAsDataURL(input.files[0]);
    }
}
