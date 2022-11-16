window.onload = () => {
	$('#sendbutton').click(() => {
		imagebox = $('#imagebox')
		prediction = $('#prediction')
		prediction.textContent = 'Procesando...';
		input = $('#imageinput')[0]
        console.log(input.files[0])
		if(input.files && input.files[0])
		{
			let formData = new FormData();
			formData.append('image' , input.files[0]);
			console.log(formData);
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
					prediction.textContent = data['text'];
				}
			});
		}
	});
};

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