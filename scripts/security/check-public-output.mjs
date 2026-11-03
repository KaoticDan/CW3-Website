import {readdir,readFile} from 'node:fs/promises';
import path from 'node:path';
const forbidden=/(^|\/)(\.env(?:\..*)?|\.git|id_rsa|id_ed25519|.*\.(?:pem|key|p12|pfx))$/i;
async function walk(dir){for(const entry of await readdir(dir,{withFileTypes:true})){const file=path.join(dir,entry.name);if(entry.isSymbolicLink())throw Error('Public output contains a symbolic link: '+file);if(forbidden.test(file.replaceAll('\\','/')))throw Error('Private material in public output: '+file);if(entry.isDirectory())await walk(file);}}
await walk('public');
if(process.argv.includes('--static')){const config=JSON.parse(await readFile('vercel.json','utf8'));if(config.outputDirectory!=='public'||config.framework!==null)throw Error('Review static deployment boundary before changing output');const index=await readFile('public/index.html','utf8');if(!/<html[\s>]/i.test(index))throw Error('Static home page missing');}
console.log('Public output boundary checked; this does not audit vendored JavaScript or hosted storage.');
