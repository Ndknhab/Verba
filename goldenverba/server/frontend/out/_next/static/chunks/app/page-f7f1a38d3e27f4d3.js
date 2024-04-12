(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[931],{87094:function(e,t,r){Promise.resolve().then(r.bind(r,19593))},19593:function(e,t,r){"use strict";r.r(t),r.d(t,{default:function(){return h}});var s=r(57437),n=r(2265),a=r(58177),i=r(30505),l=r(8603),c=r(14063),o=e=>{let{Icon:t,iconSize:r,title:n,currentPage:a,setPage:i,setCurrentPage:l}=e;return(0,s.jsxs)("button",{className:"btn md:btn-sm lg:btn-md flex flex-grow items-center justify-center border-none ".concat(a===i?"bg-primary-verba hover:bg-white":"bg-verba-bg text-text-alt-verba"),onClick:e=>{l(i)},children:[(0,s.jsx)(t,{size:r}),(0,s.jsx)("p",{className:"md:text-xs lg:text-sm sm:hidden md:flex",children:n})]})};async function m(){try{let e=await fetch("https://api.github.com/repos/weaviate/verba",{method:"GET"}),t=await e.json();if(t)return console.log("Stars "+t.stargazers_count),t.stargazers_count;return 0}catch(e){return console.error("Failed to perform search:",e),0}}let u=e=>e>=1e3?(e/1e3).toFixed(1).replace(/\.0$/,"")+"k":e.toString();var d=e=>{let{imageSrc:t,title:r,subtitle:d,version:x,currentPage:g,setCurrentPage:h}=e,[f,b]=(0,n.useState)("0");return(0,n.useEffect)(()=>{(async()=>{try{let e=await m();if(e){let t=u(e);console.log(t),b(t)}}catch(e){console.error("Failed to fetch GitHub stars:",e)}})()},[]),(0,s.jsxs)("div",{className:"flex justify-between items-center mb-10",children:[(0,s.jsxs)("div",{className:"sm:hidden md:flex flex-row items-center gap-5",children:[(0,s.jsx)("img",{src:t,width:80,className:"sm:hidden md:flex shadow-xl rounded-lg"}),(0,s.jsxs)("div",{className:"sm:hidden md:flex md:flex-col lg:flex-row lg:items-end justify-center lg:gap-3",children:[(0,s.jsx)("p",{className:" text-4xl text-text-verba",children:r}),(0,s.jsx)("p",{className:"text-base text-text-alt-verba font-light",children:d})]})]}),(0,s.jsxs)("div",{className:"flex flex-row justify-center md:justify-end items-center",children:[(0,s.jsx)("div",{className:"hidden sm:block sm:h-[3vh] lg:h-[5vh] bg-text-alt-verba w-px sm:mx-2 md:mx-4"}),(0,s.jsxs)("div",{className:"flex flex-row items-center sm:gap-1 lg:gap-5 justify-between",children:[(0,s.jsx)(o,{Icon:a.utr,iconSize:18,title:"Chat",currentPage:g,setCurrentPage:h,setPage:"CHAT"}),(0,s.jsx)(o,{Icon:a.emU,iconSize:18,title:"Documents",currentPage:g,setCurrentPage:h,setPage:"DOCUMENTS"}),(0,s.jsx)(o,{Icon:i.lLR,iconSize:18,title:"Status",currentPage:g,setCurrentPage:h,setPage:"STATUS"})]}),(0,s.jsx)("div",{className:"hidden sm:block sm:h-[3vh] lg:h-[5vh] bg-text-alt-verba w-px sm:mx-2 md:mx-4"}),(0,s.jsxs)("div",{className:"flex flex-row items-center sm:gap-1 lg:gap-5 justify-between",children:[(0,s.jsx)(o,{Icon:l.Lgw,iconSize:18,title:"Add Documents",currentPage:g,setCurrentPage:h,setPage:"ADD"}),(0,s.jsx)(o,{Icon:a.LTV,iconSize:18,title:"RAG",currentPage:g,setCurrentPage:h,setPage:"RAG"})]}),(0,s.jsx)("div",{className:"hidden sm:block sm:h-[3vh] lg:h-[5vh] bg-text-alt-verba w-px sm:mx-2 md:mx-4"}),(0,s.jsxs)("div",{className:"flex flex-row items-center sm:gap-1 lg:gap-5 justify-between",children:[(0,s.jsx)(o,{Icon:a.zfW,iconSize:18,title:"Settings",currentPage:g,setCurrentPage:h,setPage:"SETTINGS"}),(0,s.jsxs)("button",{className:"btn md:btn-sm lg:btn-md flex items-center justify-center border-none bg-secondary-verba hover:bg-white",onClick:()=>{window.open("https://github.com/weaviate/verba","_blank","noopener,noreferrer")},children:[(0,s.jsx)(c.hJX,{size:18,className:""}),(0,s.jsx)("p",{className:"text-xs sm:hidden md:flex ",children:f})]}),(0,s.jsx)("p",{className:"text-sm text-text-alt-verba hidden md:flex",children:x})]})]})]})},x=e=>{let{}=e;return(0,s.jsx)("div",{className:"flex justify-between items-center",children:(0,s.jsx)("div",{})})};let g={customization:{title:{text:"Verba"},subtitle:{text:"The Golden RAGtriever"},image:{encoding:"https://github.com/weaviate/Verba/blob/main/frontend/public/favicon.png?raw=true"}}};function h(){let[e,t]=(0,n.useState)("CHAT"),[r,a]=(0,n.useState)(g);return(0,s.jsxs)("main",{className:"min-h-screen p-2 md:p-6","data-theme":"light",children:[(0,s.jsx)(d,{title:r.customization.title.text,subtitle:r.customization.subtitle.text,imageSrc:r.customization.image.encoding,version:"v1.0.0",currentPage:e,setCurrentPage:t}),"SETTINGS"===e&&(0,s.jsx)(x,{})]})}},39350:function(e,t,r){"use strict";r.d(t,{w_:function(){return c}});var s=r(2265),n={color:void 0,size:void 0,className:void 0,style:void 0,attr:void 0},a=s.createContext&&s.createContext(n),i=function(){return(i=Object.assign||function(e){for(var t,r=1,s=arguments.length;r<s;r++)for(var n in t=arguments[r])Object.prototype.hasOwnProperty.call(t,n)&&(e[n]=t[n]);return e}).apply(this,arguments)},l=function(e,t){var r={};for(var s in e)Object.prototype.hasOwnProperty.call(e,s)&&0>t.indexOf(s)&&(r[s]=e[s]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols)for(var n=0,s=Object.getOwnPropertySymbols(e);n<s.length;n++)0>t.indexOf(s[n])&&Object.prototype.propertyIsEnumerable.call(e,s[n])&&(r[s[n]]=e[s[n]]);return r};function c(e){return function(t){return s.createElement(o,i({attr:i({},e.attr)},t),function e(t){return t&&t.map(function(t,r){return s.createElement(t.tag,i({key:r},t.attr),e(t.child))})}(e.child))}}function o(e){var t=function(t){var r,n=e.attr,a=e.size,c=e.title,o=l(e,["attr","size","title"]),m=a||t.size||"1em";return t.className&&(r=t.className),e.className&&(r=(r?r+" ":"")+e.className),s.createElement("svg",i({stroke:"currentColor",fill:"currentColor",strokeWidth:"0"},t.attr,n,o,{className:r,style:i(i({color:e.color||t.color},t.style),e.style),height:m,width:m,xmlns:"http://www.w3.org/2000/svg"}),c&&s.createElement("title",null,c),e.children)};return void 0!==a?s.createElement(a.Consumer,null,function(e){return t(e)}):t(n)}}},function(e){e.O(0,[420,190,400,982,971,23,744],function(){return e(e.s=87094)}),_N_E=e.O()}]);