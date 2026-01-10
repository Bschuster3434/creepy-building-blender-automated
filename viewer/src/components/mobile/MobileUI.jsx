import React, { useState, useCallback } from 'react'

/**
 * Mobile-friendly controls panel
 * Collapsible header with expandable model selector
 */
export function MobileControlsPanel({
  models,
  selectedModel,
  onModelSelect,
  isFirstPerson,
  onToggleMode
}) {
  const [isExpanded, setIsExpanded] = useState(false)
  const [showModelSelector, setShowModelSelector] = useState(false)

  const currentModel = models[selectedModel]

  return (
    <>
      {/* Compact header bar */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        background: 'rgba(0, 0, 0, 0.85)',
        padding: '12px 16px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        zIndex: 100,
      }}>
        {/* Model selector button */}
        <button
          onClick={() => setShowModelSelector(true)}
          style={{
            background: 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 8,
            padding: '10px 14px',
            color: 'white',
            fontSize: 13,
            display: 'flex',
            alignItems: 'center',
            gap: 8,
            maxWidth: '60%',
            overflow: 'hidden',
          }}
        >
          <span style={{
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
          }}>
            {currentModel?.name || 'Select Model'}
          </span>
          <span style={{ opacity: 0.6 }}>▼</span>
        </button>

        {/* Mode toggle button */}
        <button
          onClick={onToggleMode}
          style={{
            background: isFirstPerson
              ? 'rgba(74, 111, 165, 0.9)'
              : 'rgba(255, 255, 255, 0.1)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: 8,
            padding: '10px 16px',
            color: 'white',
            fontSize: 13,
            fontWeight: 'bold',
            minWidth: 100,
          }}
        >
          {isFirstPerson ? 'First Person' : 'Orbit'}
        </button>
      </div>

      {/* Full-screen model selector modal */}
      {showModelSelector && (
        <MobileModelSelector
          models={models}
          selectedModel={selectedModel}
          onSelect={(index) => {
            onModelSelect(index)
            setShowModelSelector(false)
          }}
          onClose={() => setShowModelSelector(false)}
        />
      )}
    </>
  )
}

/**
 * Full-screen model selector for mobile
 * Searchable list with grouped models
 */
function MobileModelSelector({ models, selectedModel, onSelect, onClose }) {
  const [searchTerm, setSearchTerm] = useState('')

  // Group models by phase
  const groupedModels = React.useMemo(() => {
    const groups = {}
    models.forEach((model, index) => {
      // Extract group from model name (e.g., "Phase 3", "Phase 2", etc.)
      const match = model.name.match(/^(Phase \d+[A-C]?|Work|Early)/i)
      const group = match ? match[1] : 'Other'

      if (!groups[group]) groups[group] = []
      groups[group].push({ ...model, index })
    })
    return groups
  }, [models])

  // Filter models by search term
  const filteredGroups = React.useMemo(() => {
    if (!searchTerm) return groupedModels

    const filtered = {}
    Object.entries(groupedModels).forEach(([group, items]) => {
      const matchingItems = items.filter(item =>
        item.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
      if (matchingItems.length > 0) {
        filtered[group] = matchingItems
      }
    })
    return filtered
  }, [groupedModels, searchTerm])

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.95)',
      zIndex: 200,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Header */}
      <div style={{
        padding: '16px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}>
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            fontSize: 24,
            padding: '8px',
            cursor: 'pointer',
          }}
        >
          ←
        </button>
        <h2 style={{ color: 'white', margin: 0, fontSize: 18, flex: 1 }}>
          Select Model
        </h2>
        <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: 13 }}>
          {models.length} models
        </span>
      </div>

      {/* Search input */}
      <div style={{ padding: '12px 16px' }}>
        <input
          type="text"
          placeholder="Search models..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            width: '100%',
            padding: '14px 16px',
            borderRadius: 8,
            border: '1px solid rgba(255, 255, 255, 0.2)',
            background: 'rgba(255, 255, 255, 0.1)',
            color: 'white',
            fontSize: 16,
            outline: 'none',
          }}
        />
      </div>

      {/* Model list */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: '0 16px 16px',
      }}>
        {Object.entries(filteredGroups).map(([group, items]) => (
          <div key={group} style={{ marginBottom: 20 }}>
            <h3 style={{
              color: 'rgba(255, 255, 255, 0.6)',
              fontSize: 12,
              textTransform: 'uppercase',
              letterSpacing: 1,
              margin: '0 0 10px 0',
              padding: '8px 0',
              borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
            }}>
              {group}
            </h3>
            {items.map((model) => (
              <button
                key={model.index}
                onClick={() => onSelect(model.index)}
                style={{
                  width: '100%',
                  padding: '16px',
                  marginBottom: 8,
                  borderRadius: 8,
                  border: model.index === selectedModel
                    ? '2px solid rgba(74, 111, 165, 0.8)'
                    : '1px solid rgba(255, 255, 255, 0.1)',
                  background: model.index === selectedModel
                    ? 'rgba(74, 111, 165, 0.3)'
                    : 'rgba(255, 255, 255, 0.05)',
                  color: 'white',
                  fontSize: 15,
                  textAlign: 'left',
                  cursor: 'pointer',
                }}
              >
                {model.name}
              </button>
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Mobile-friendly reference panel
 * Bottom sheet style with swipe-to-close
 */
export function MobileReferencePanel({
  references,
  activeCategory,
  onCategoryChange,
  onSelectImage,
  onClose,
  onOpenGallery
}) {
  const categoryData = references[activeCategory]

  return (
    <div style={{
      position: 'fixed',
      bottom: 0,
      left: 0,
      right: 0,
      maxHeight: '70vh',
      background: 'rgba(0, 0, 0, 0.95)',
      borderRadius: '20px 20px 0 0',
      display: 'flex',
      flexDirection: 'column',
      zIndex: 150,
    }}>
      {/* Drag handle */}
      <div style={{
        padding: '12px',
        display: 'flex',
        justifyContent: 'center',
      }}>
        <div style={{
          width: 40,
          height: 4,
          background: 'rgba(255, 255, 255, 0.3)',
          borderRadius: 2,
        }} />
      </div>

      {/* Header */}
      <div style={{
        padding: '0 16px 12px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <h3 style={{ color: 'white', margin: 0, fontSize: 16 }}>
          Reference Images
        </h3>
        <div style={{ display: 'flex', gap: 10 }}>
          <button
            onClick={onOpenGallery}
            style={{
              background: 'rgba(255, 255, 255, 0.1)',
              border: 'none',
              borderRadius: 6,
              padding: '8px 14px',
              color: 'white',
              fontSize: 13,
            }}
          >
            View All
          </button>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: 'white',
              fontSize: 20,
              padding: '4px 8px',
            }}
          >
            ×
          </button>
        </div>
      </div>

      {/* Category tabs - horizontal scroll */}
      <div style={{
        display: 'flex',
        padding: '0 16px',
        gap: 8,
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        overflowX: 'auto',
        WebkitOverflowScrolling: 'touch',
      }}>
        {Object.keys(references).map(category => (
          <button
            key={category}
            onClick={() => onCategoryChange(category)}
            style={{
              background: activeCategory === category
                ? 'rgba(74, 111, 165, 0.8)'
                : 'transparent',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              padding: '12px 16px',
              color: 'white',
              fontSize: 14,
              whiteSpace: 'nowrap',
              opacity: activeCategory === category ? 1 : 0.6,
            }}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Thumbnails - horizontal scroll per subcategory */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: 16,
      }}>
        {Object.entries(categoryData.subcategories).map(([subcategory, images]) => (
          <div key={subcategory} style={{ marginBottom: 20 }}>
            <p style={{
              color: 'rgba(255, 255, 255, 0.6)',
              fontSize: 12,
              margin: '0 0 10px 0',
            }}>
              {subcategory}
            </p>
            <div style={{
              display: 'flex',
              gap: 10,
              overflowX: 'auto',
              WebkitOverflowScrolling: 'touch',
              paddingBottom: 10,
            }}>
              {images.map(image => (
                <div
                  key={image.file}
                  onClick={() => onSelectImage({ ...image, category: activeCategory, subcategory })}
                  style={{
                    flexShrink: 0,
                    width: 100,
                    height: 75,
                    borderRadius: 8,
                    overflow: 'hidden',
                    cursor: 'pointer',
                  }}
                >
                  <img
                    src={image.file}
                    alt={image.name}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                    }}
                    loading="lazy"
                  />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Mobile reference gallery - full screen
 */
export function MobileReferenceGallery({ references, onSelectImage, onClose }) {
  const [activeCategory, setActiveCategory] = useState('Exterior')

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(0, 0, 0, 0.95)',
      zIndex: 200,
      display: 'flex',
      flexDirection: 'column',
    }}>
      {/* Header */}
      <div style={{
        padding: '16px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        display: 'flex',
        alignItems: 'center',
        gap: 12,
      }}>
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            fontSize: 24,
            padding: '8px',
          }}
        >
          ←
        </button>
        <h2 style={{ color: 'white', margin: 0, fontSize: 18 }}>
          Reference Images
        </h2>
      </div>

      {/* Category tabs */}
      <div style={{
        display: 'flex',
        padding: '0 16px',
        gap: 8,
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        overflowX: 'auto',
      }}>
        {Object.keys(references).map(category => (
          <button
            key={category}
            onClick={() => setActiveCategory(category)}
            style={{
              background: activeCategory === category
                ? 'rgba(74, 111, 165, 0.8)'
                : 'transparent',
              border: 'none',
              borderRadius: '8px 8px 0 0',
              padding: '12px 16px',
              color: 'white',
              fontSize: 14,
              whiteSpace: 'nowrap',
            }}
          >
            {category}
          </button>
        ))}
      </div>

      {/* Images grid */}
      <div style={{
        flex: 1,
        overflowY: 'auto',
        padding: 16,
      }}>
        {Object.entries(references[activeCategory].subcategories).map(([subcategory, images]) => (
          <div key={subcategory} style={{ marginBottom: 24 }}>
            <h4 style={{
              color: 'rgba(255, 255, 255, 0.6)',
              fontSize: 13,
              margin: '0 0 12px 0',
            }}>
              {subcategory}
            </h4>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: 10,
            }}>
              {images.map(image => (
                <div
                  key={image.file}
                  onClick={() => onSelectImage({ ...image, category: activeCategory, subcategory })}
                  style={{
                    aspectRatio: '4/3',
                    borderRadius: 8,
                    overflow: 'hidden',
                    cursor: 'pointer',
                  }}
                >
                  <img
                    src={image.file}
                    alt={image.name}
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                    }}
                    loading="lazy"
                  />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

/**
 * Mobile lightbox for full-screen image viewing
 */
export function MobileLightbox({ image, allImages, onClose, onNavigate }) {
  const currentIndex = allImages.findIndex(img => img.file === image.file)

  const handleSwipe = useCallback((direction) => {
    if (direction === 'left' && currentIndex < allImages.length - 1) {
      onNavigate(allImages[currentIndex + 1])
    } else if (direction === 'right' && currentIndex > 0) {
      onNavigate(allImages[currentIndex - 1])
    }
  }, [currentIndex, allImages, onNavigate])

  // Simple swipe detection
  const touchStartRef = React.useRef(null)

  const handleTouchStart = (e) => {
    touchStartRef.current = e.touches[0].clientX
  }

  const handleTouchEnd = (e) => {
    if (touchStartRef.current === null) return

    const touchEnd = e.changedTouches[0].clientX
    const diff = touchStartRef.current - touchEnd

    if (Math.abs(diff) > 50) {
      handleSwipe(diff > 0 ? 'left' : 'right')
    }

    touchStartRef.current = null
  }

  return (
    <div
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.98)',
        zIndex: 300,
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Header */}
      <div style={{
        padding: '16px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
      }}>
        <button
          onClick={onClose}
          style={{
            background: 'none',
            border: 'none',
            color: 'white',
            fontSize: 24,
            padding: '8px',
          }}
        >
          ←
        </button>
        <div style={{ color: 'white', textAlign: 'center' }}>
          <p style={{ margin: 0, fontSize: 14 }}>{image.name}</p>
          <p style={{ margin: '4px 0 0', fontSize: 12, opacity: 0.6 }}>
            {currentIndex + 1} / {allImages.length}
          </p>
        </div>
        <div style={{ width: 40 }} /> {/* Spacer for centering */}
      </div>

      {/* Image */}
      <div style={{
        flex: 1,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 16,
      }}>
        <img
          src={image.file}
          alt={image.name}
          style={{
            maxWidth: '100%',
            maxHeight: '100%',
            objectFit: 'contain',
          }}
        />
      </div>

      {/* Swipe hint */}
      <div style={{
        padding: '16px',
        textAlign: 'center',
        color: 'rgba(255, 255, 255, 0.5)',
        fontSize: 12,
      }}>
        Swipe to navigate
      </div>
    </div>
  )
}

/**
 * Mobile floating action button for references
 */
export function MobileRefButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        position: 'absolute',
        bottom: 30,
        left: '50%',
        transform: 'translateX(-50%)',
        background: 'rgba(0, 0, 0, 0.8)',
        border: '1px solid rgba(255, 255, 255, 0.2)',
        borderRadius: 25,
        padding: '12px 20px',
        color: 'white',
        fontSize: 13,
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        zIndex: 50,
      }}
    >
      <span>📷</span>
      <span>References</span>
    </button>
  )
}

/**
 * Mobile first-person help overlay
 * Shows touch controls hints
 */
export function MobileFirstPersonHelp({ onDismiss }) {
  return (
    <div
      onClick={onDismiss}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.85)',
        zIndex: 250,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 30,
      }}
    >
      <h2 style={{ color: 'white', marginBottom: 30 }}>First-Person Controls</h2>

      <div style={{ color: 'white', fontSize: 16, lineHeight: 2 }}>
        <p>👆 <strong>Touch & drag</strong> screen to look around</p>
        <p>🕹️ <strong>Left joystick</strong> to move</p>
        <p>🚪 <strong>Action button</strong> to interact with doors</p>
      </div>

      <button
        style={{
          marginTop: 40,
          background: 'rgba(74, 111, 165, 0.9)',
          border: 'none',
          borderRadius: 8,
          padding: '14px 40px',
          color: 'white',
          fontSize: 16,
          fontWeight: 'bold',
        }}
      >
        Tap anywhere to start
      </button>
    </div>
  )
}
