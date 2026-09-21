import * as THREE from 'three';

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000510);

const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Molecular visualization
const geometry = new THREE.SphereGeometry(0.1, 32, 32);
const material = new THREE.MeshStandardMaterial({ 
  color: 0x00ffff, 
  emissive: 0x004444,
  transparent: true,
  opacity: 0.8
});

const molecules = [];
for (let i = 0; i < 500; i++) {
  const mesh = new THREE.Mesh(geometry, material);
  mesh.position.set(
    (Math.random() - 0.5) * 10,
    (Math.random() - 0.5) * 10,
    (Math.random() - 0.5) * 10
  );
  scene.add(mesh);
  molecules.push(mesh);
}

const light = new THREE.PointLight(0xffffff, 1, 100);
light.position.set(0, 0, 10);
scene.add(light);

function animate() {
  requestAnimationFrame(animate);
  molecules.forEach((m, i) => {
    m.position.y += Math.sin(Date.now() * 0.001 + i) * 0.001;
    m.rotation.x += 0.01;
    m.rotation.y += 0.01;
  });
  renderer.render(scene, camera);
}

animate();

window.addEventListener('resize', () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// UI Overlay
const ui = document.createElement('div');
ui.style.cssText = 'position:absolute;top:20px;left:20px;color:#00ffff;font-family:sans-serif;z-index:10;';
ui.innerHTML = '<h1>TABEEBY Nano Visualization</h1><p>Atomic Resolution - Molecular Surgery Field</p>';
document.body.appendChild(ui);
