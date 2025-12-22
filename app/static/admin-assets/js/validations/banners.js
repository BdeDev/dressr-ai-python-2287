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

		media: {
			required: "Please upload media",
            accept: "jpg,png,jpeg,mp4",
			},
		},
	});  

$("#edit-banners").validate({
	ignore: [],
	rules: {
		title: {
			required: true,
			},
		image: {
			required: false,
			},
		},
	messages: {
		title: {
			required: "Please Enter Name",
			},

		media: {
			required: "Please upload media",
            accept: "Please upload file in these format only (jpg, jpeg, png,mp4)"
			},
		},
})