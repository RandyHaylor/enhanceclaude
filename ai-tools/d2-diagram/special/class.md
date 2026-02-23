# Class Diagrams

- Set `shape: class` on a container
- Visibility prefix: `+` public, `-` private, `#` protected
- Inheritance / implementation drawn as connections with labels

```d2
Animal: {
  shape: class
  +name: string
  -secret: string
  +speak(): void
  #move(speed: int): void
}

Dog: {
  shape: class
  +breed: string
  +fetch(): void
}

Animal -> Dog: extends
IAnimal -> Animal: implements
Service -> Repository: injects {style.stroke-dash: 3}
```
