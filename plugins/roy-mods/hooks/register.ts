import type { Register } from 'claude-code'

import { register as trackingList } from '../mods/tracking-list/register'

// One hooks module per plugin: each mod in mods/<name>/ is registered here.
export const register: Register = (on, options) => {
  trackingList(on, options)
}
