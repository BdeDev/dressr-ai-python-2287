$("#add-banners").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		image: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Name",
			},

		image: {
			required: "Please upload image",
            accept: "jpg,png,jpeg",
			},
		},
	});  


$("#edit-banner").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		image: {
			required: true,
			},
		},
	messages: {
		title: {
			required: "Please Enter Name",
			},

		image: {
			required: "Please upload image",
            accept: "Please upload file in these format only (jpg, jpeg, png)"
			},
		},
})