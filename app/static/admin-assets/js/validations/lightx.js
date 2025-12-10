$("#add-lightx-creds").validate({
	ignore: [],
	rules: {
		api_key: {
			required: true,
			},
		},
	messages: {
		api_key: {
			required: "Please Enter API Key",
			},
		},
	});  


$("#edit-lightx-creds").validate({
	ignore: [],
	rules: {
		api_key: {
			required: true,
			},
		},
	messages: {
		api_key: {
			required: "Please Enter API Key",
			},
		
		},
    })