let blog_posts = 
[
    {
        name: "First Blog",
        description: "My first ever blog on my own site.",
        date: new Date("2021-03-18"),
        path: "./content/blog/FirstBlog/FirstBlog.html",
        picture: null,
    },
    {
        name: "Minimalism",
        description: "My thoughts on moving to suckless software and using arch for the past few months.",
        date: new Date("2021-03-18"),
        path: "./content/blog/Minimalism/Minimalism.html",
        picture: null,
    },
    {
        name: "Privacy",
        description: "My thoughts on privacy and the survaillance cage we built for ourselves (OMG literally 1984!!!!!!!!).",
        date: new Date("2021-03-18"),
        path: "./content/blog/Privacy/Privacy.html",
        picture: "./content/blog/Privacy/Privacy.jpeg"
    }

];

const sorted_blogs = blog_posts.slice().sort((a, b) => b.date - a.date);

let final_html_blogs = "";
if (document.title == "PanTech" && blog_posts.length >= 3) {
    for(let j = 0; j < 3; j ++) {
        let a = sorted_blogs[j]
        if (a.picture == null){
            final_html_blogs += `<section><a href="${a.path}"><h3>${a.name}</h3></a><p>${a.description}</p></section>`
        } else {
            final_html_blogs += `<a href="${a.path}"><h3>${a.name}</h3></a><section><figure><a href="${a.path}"><img src="${a.picture}"></a><figcaption>${a.description}</figcaption></figure></section>`
        }
    };
} else {
    for(let j = 0; j < blog_posts.length; j ++) {
        let a = sorted_blogs[j]
        if (a.picture == null){
            final_html_blogs += `<section><a href="${a.path}"><h2>${a.name}</h2></a><p>${a.description}</p></section>`
        } else {
            final_html_blogs += `<section><a href="${a.path}"><h2>${a.name}</h2></a><figure><a href="${a.path}"><img src="${a.picture}" alt=""></a><figcaption>${a.description}</figcaption></figure></section>`
        }
    };
}


const blog = document.getElementById("blog")
blog.innerHTML = final_html_blogs