import { useEffect, useRef } from 'react'
import * as THREE from 'three'

function mapToScene(x, y) {
  const nx = (x - 150) / 10
  const nz = (y - 100) / 10
  return { x: nx, z: nz }
}

export function ThreeScene({
  emergency,
  phase,
  drone,
  fireIntensity,
  floodLevel,
  materialsInside,
  materialsOutside,
}) {
  const mountRef = useRef(null)
  const sprayUntilRef = useRef(0)
  const stateRef = useRef({
    emergency,
    phase,
    drone,
    fireIntensity,
    floodLevel,
    materialsInside,
    materialsOutside,
  })
  stateRef.current = {
    emergency,
    phase,
    drone,
    fireIntensity,
    floodLevel,
    materialsInside,
    materialsOutside,
  }

  useEffect(() => {
    const mount = mountRef.current
    if (!mount) return undefined

    const scene = new THREE.Scene()
    scene.background = new THREE.Color('#0b1327')

    const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 100)
    camera.position.set(0, 6.5, 10)
    camera.lookAt(0, 0, 0)

    const renderer = new THREE.WebGLRenderer({ antialias: true })
    renderer.setPixelRatio(window.devicePixelRatio || 1)
    mount.appendChild(renderer.domElement)

    const ambient = new THREE.AmbientLight(0xffffff, 0.55)
    scene.add(ambient)
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.6)
    dirLight.position.set(6, 10, 4)
    scene.add(dirLight)
    const fireLight = new THREE.PointLight(0xff7a3a, 0.0, 12, 2)
    fireLight.position.set(-1.6, 2.4, -0.3)
    scene.add(fireLight)

    const ground = new THREE.Mesh(
      new THREE.PlaneGeometry(40, 30),
      new THREE.MeshStandardMaterial({ color: '#0f172a' })
    )
    ground.rotation.x = -Math.PI / 2
    ground.position.y = -0.01
    scene.add(ground)

    const houseGroup = new THREE.Group()
    const houseBodyMaterial = new THREE.MeshStandardMaterial({ color: '#e2e8f0' })
    const houseBody = new THREE.Mesh(
      new THREE.BoxGeometry(4.2, 2.2, 3.2),
      houseBodyMaterial
    )
    houseBody.position.y = 1.1
    houseGroup.add(houseBody)
    const roofMaterial = new THREE.MeshStandardMaterial({ color: '#be123c' })
    const roof = new THREE.Mesh(
      new THREE.ConeGeometry(3.6, 1.6, 4),
      roofMaterial
    )
    roof.rotation.y = Math.PI / 4
    roof.position.y = 3.1
    houseGroup.add(roof)
    houseGroup.position.set(-2, 0, -1)
    scene.add(houseGroup)

    const droneTexture = new THREE.TextureLoader().load('/drone.png')
    const droneSpriteMaterial = new THREE.SpriteMaterial({ map: droneTexture, transparent: true })
    const droneMesh = new THREE.Sprite(droneSpriteMaterial)
    droneMesh.scale.set(1.3, 1.3, 1)
    droneMesh.position.set(3, 2.2, 3)
    scene.add(droneMesh)

    const fireMesh = new THREE.Mesh(
      new THREE.ConeGeometry(0.6, 1.6, 10),
      new THREE.MeshStandardMaterial({ color: '#fb7185', emissive: '#fb923c' })
    )
    fireMesh.position.set(-1.8, 1.7, -0.2)
    scene.add(fireMesh)

    const smokeMesh = new THREE.Mesh(
      new THREE.ConeGeometry(1.0, 2.6, 10),
      new THREE.MeshStandardMaterial({
        color: '#64748b',
        transparent: true,
        opacity: 0.2,
      })
    )
    smokeMesh.position.set(-1.8, 3.3, -0.2)
    smokeMesh.visible = false
    scene.add(smokeMesh)

    const waterPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(40, 30),
      new THREE.MeshStandardMaterial({
        color: '#38bdf8',
        transparent: true,
        opacity: 0.35,
      })
    )
    waterPlane.rotation.x = -Math.PI / 2
    waterPlane.position.y = -0.01
    scene.add(waterPlane)

    const waterPlaneBaseY = -0.02

    const video = document.createElement('video')
    video.src = '/water.mp4'
    video.loop = true
    video.muted = true
    video.playsInline = true
    video.autoplay = true

    const videoTexture = new THREE.VideoTexture(video)
    videoTexture.minFilter = THREE.LinearFilter
    videoTexture.magFilter = THREE.LinearFilter
    videoTexture.colorSpace = THREE.SRGBColorSpace

    const sprayPlane = new THREE.Mesh(
      new THREE.PlaneGeometry(3.4, 2.4),
      new THREE.MeshBasicMaterial({
        map: videoTexture,
        transparent: true,
        opacity: 0.85,
        side: THREE.DoubleSide,
      })
    )
    sprayPlane.position.set(-1.8, 4.2, -0.2)
    sprayPlane.rotation.x = -Math.PI / 3.2
    sprayPlane.visible = false
    scene.add(sprayPlane)

    const splashGroup = new THREE.Group()
    scene.add(splashGroup)

    const materialInsideGroup = new THREE.Group()
    const materialOutsideGroup = new THREE.Group()
    scene.add(materialInsideGroup)
    scene.add(materialOutsideGroup)

    const helperDroneGroup = new THREE.Group()
    scene.add(helperDroneGroup)

    const insideSlots = [
      new THREE.Vector3(-0.6, 0.4, -2.6),
      new THREE.Vector3(0.2, 0.4, -2.2),
      new THREE.Vector3(-1.2, 0.4, -2.0),
      new THREE.Vector3(0.6, 0.4, -2.6),
      new THREE.Vector3(-0.2, 0.4, -1.8),
      new THREE.Vector3(1.0, 0.4, -2.0),
    ]
    const outsideSlots = [
      new THREE.Vector3(6.0, 0.4, 2.4),
      new THREE.Vector3(5.2, 0.4, 2.0),
      new THREE.Vector3(6.4, 0.4, 1.6),
      new THREE.Vector3(5.6, 0.4, 1.2),
      new THREE.Vector3(6.8, 0.4, 0.8),
      new THREE.Vector3(5.0, 0.4, 0.6),
    ]

    const createCrate = (color) => new THREE.Mesh(
      new THREE.BoxGeometry(0.45, 0.35, 0.35),
      new THREE.MeshStandardMaterial({ color })
    )

    const handleResize = () => {
      if (!mount) return
      const { clientWidth, clientHeight } = mount
      if (clientWidth === 0 || clientHeight === 0) return
      camera.aspect = clientWidth / clientHeight
      camera.updateProjectionMatrix()
      renderer.setSize(clientWidth, clientHeight, false)
    }

    const resizeObserver = new ResizeObserver(handleResize)
    resizeObserver.observe(mount)
    handleResize()

    let frameId
    const animate = () => {
      const {
        emergency,
        phase,
        drone,
        fireIntensity,
        floodLevel,
        materialsInside,
        materialsOutside,
      } = stateRef.current
      const fireScale = Math.max(0.15, fireIntensity / 100)
      fireMesh.visible = fireIntensity > 0
      fireMesh.scale.set(1, fireScale * 1.6, 1)
      fireMesh.rotation.y += 0.02

      if (fireIntensity > 0) {
        const heat = Math.min(1, fireIntensity / 100)
        const flicker = 0.08 + Math.sin(Date.now() * 0.008) * 0.04
        houseBodyMaterial.color.setHSL(0.03, 0.55, 0.85 - heat * 0.25)
        houseBodyMaterial.emissive.setHex(0x7a2b1a)
        houseBodyMaterial.emissiveIntensity = heat * 0.4 + flicker
        roofMaterial.emissive.setHex(0x8a2412)
        roofMaterial.emissiveIntensity = heat * 0.6 + flicker
        fireLight.intensity = 0.6 + heat * 1.2 + flicker
        smokeMesh.visible = true
        smokeMesh.scale.set(1, 0.9 + heat * 0.6, 1)
        smokeMesh.position.y = 3.1 + heat * 0.6
        smokeMesh.material.opacity = 0.12 + heat * 0.22
      } else {
        houseBodyMaterial.emissiveIntensity = 0
        roofMaterial.emissiveIntensity = 0
        fireLight.intensity = 0
        smokeMesh.visible = false
      }

      waterPlane.visible = floodLevel > 0
      const wave = Math.sin(Date.now() * 0.0025) * 0.06
      waterPlane.position.y = waterPlaneBaseY + (floodLevel / 100) * 1.2 + wave

      const mapped = mapToScene(drone.x, drone.y)
      droneMesh.position.x = mapped.x
      droneMesh.position.z = mapped.z
      droneMesh.position.y = 2.2 + Math.sin(Date.now() * 0.004) * 0.08

      const spraying = emergency === 'fire' && phase === 'deploying_water'
      if (spraying) {
        sprayUntilRef.current = Date.now() + 2500
      }
      const sprayActive = Date.now() < sprayUntilRef.current
      sprayPlane.visible = sprayActive
      if (sprayActive && video.paused) {
        video.play().catch(() => {})
      }

      splashGroup.clear()
      if (sprayActive) {
        const impact = new THREE.Vector3(-1.6, 1.0, -0.1)
        const now = Date.now()
        for (let i = 0; i < 8; i += 1) {
          const drop = new THREE.Mesh(
            new THREE.SphereGeometry(0.06, 8, 8),
            new THREE.MeshStandardMaterial({ color: '#7dd3fc', emissive: '#38bdf8' })
          )
          const angle = (i / 8) * Math.PI * 2
          const radius = 0.15 + (i % 3) * 0.05
          const pulse = (Math.sin((now / 120) + i) + 1) * 0.5
          drop.position.set(
            impact.x + Math.cos(angle) * radius,
            impact.y + 0.06 + pulse * 0.08,
            impact.z + Math.sin(angle) * radius
          )
          drop.scale.setScalar(0.8 + pulse * 0.5)
          splashGroup.add(drop)
        }
      }

      materialInsideGroup.clear()
      const insideCount = Math.min(6, materialsInside || 0)
      for (let i = 0; i < insideCount; i += 1) {
        const crate = createCrate('#f59e0b')
        crate.position.copy(insideSlots[i])
        materialInsideGroup.add(crate)
      }

      materialOutsideGroup.clear()
      const outsideCount = Math.min(6, materialsOutside || 0)
      for (let i = 0; i < outsideCount; i += 1) {
        const crate = createCrate('#10b981')
        crate.position.copy(outsideSlots[i])
        materialOutsideGroup.add(crate)
      }

      helperDroneGroup.clear()
      if (phase === 'clearing_materials') {
        const helperCount = Math.min(3, insideCount)
        const now = Date.now()
        for (let i = 0; i < helperCount; i += 1) {
          const helper = new THREE.Sprite(droneSpriteMaterial.clone())
          helper.scale.set(0.9, 0.9, 1)
          const start = insideSlots[i]
          const end = outsideSlots[i]
          const t = ((now / 1000) + i * 0.35) % 1
          helper.position.lerpVectors(start, end, t)
          helper.position.y += 0.9 + Math.sin((now / 200) + i) * 0.1
          helperDroneGroup.add(helper)

          const crate = createCrate('#f59e0b')
          crate.position.set(helper.position.x, helper.position.y - 0.35, helper.position.z)
          crate.scale.set(0.6, 0.6, 0.6)
          helperDroneGroup.add(crate)
        }
      }

      renderer.render(scene, camera)
      frameId = requestAnimationFrame(animate)
    }

    animate()

    return () => {
      cancelAnimationFrame(frameId)
      resizeObserver.disconnect()
      renderer.dispose()
      video.pause()
      video.src = ''
      if (renderer.domElement.parentNode) {
        renderer.domElement.parentNode.removeChild(renderer.domElement)
      }
      scene.clear()
    }
  }, [])

  return (
    <section className="panel three-panel">
      <h2 className="title"> Response Scene</h2>
      <p className="scene-caption">Autonomous drone response rendered in Three.js.</p>
      <div className="three-canvas" ref={mountRef} />
    </section>
  )
}
