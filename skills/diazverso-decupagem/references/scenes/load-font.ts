/** Load a caller-provided licensed font once per browser page. */
const cache=new Map<string,Promise<void>>();
export function loadFont({family,url}:{family:string;url:string}):Promise<void>{
 if(!family?.trim()||!url?.trim()||url.length>4096)return Promise.reject(new Error('Provide a licensed local font URL and family'));
 if(typeof document==='undefined'||typeof FontFace==='undefined')return Promise.reject(new Error('Font loading requires the render browser'));
 const resolved=new URL(url,document.baseURI);
 if(!['http:','https:'].includes(resolved.protocol))return Promise.reject(new Error('Use a font served by the editing project'));
 const key=JSON.stringify([family,resolved.href]);
 if(cache.has(key))return cache.get(key)!;
 const promise=new FontFace(family,`url(${JSON.stringify(resolved.href)})`).load().then(font=>{document.fonts.add(font);});
 cache.set(key,promise);if(cache.size>32)cache.delete(cache.keys().next().value!);
 promise.catch(()=>{if(cache.get(key)===promise)cache.delete(key);});return promise;
}
