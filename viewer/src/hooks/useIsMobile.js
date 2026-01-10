import { useState, useEffect } from 'react'

/**
 * Hook to detect if the user is on a mobile device
 * Uses both screen size and touch capability for accurate detection
 * Only affects mobile users - desktop remains unchanged
 */
export function useIsMobile() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const checkMobile = () => {
      // Check for touch capability
      const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0

      // Check screen size (tablets and phones)
      const isSmallScreen = window.innerWidth <= 1024

      // Check user agent for mobile devices (backup check)
      const mobileUserAgent = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      )

      // Consider mobile if: has touch AND (small screen OR mobile user agent)
      setIsMobile(hasTouch && (isSmallScreen || mobileUserAgent))
    }

    // Initial check
    checkMobile()

    // Listen for resize events (orientation changes, etc.)
    window.addEventListener('resize', checkMobile)

    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  return isMobile
}

/**
 * Hook to detect device orientation
 */
export function useOrientation() {
  const [isPortrait, setIsPortrait] = useState(true)

  useEffect(() => {
    const checkOrientation = () => {
      setIsPortrait(window.innerHeight > window.innerWidth)
    }

    checkOrientation()
    window.addEventListener('resize', checkOrientation)

    return () => window.removeEventListener('resize', checkOrientation)
  }, [])

  return isPortrait
}
