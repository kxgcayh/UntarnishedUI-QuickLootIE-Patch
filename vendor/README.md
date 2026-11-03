# Build inputs

These are the unmodified files the build starts from. They are committed so a clone can rebuild the release on its own.

| file | source | SHA-256 | terms |
|---|---|---|---|
| `qlie-4.1.3/LootMenuIE.swf` | `Interface/LootMenuIE.swf` from [QuickLoot IE](https://www.nexusmods.com/skyrimspecialedition/mods/120075) 4.1.3 (identical to the copy in its Developer SDK 4.1.3) | `e2a5fdea66b0a167ca5c9349f37a7d7ab58e904d68700344aefaf6f80ec3b0e7` | GNU GPL v3 (`../LICENSE`) |
| `untarnished-1.1.3/style1/LootMenuIE.swf` | `interface/style1/LootMenuIE.swf` from [Quickloot IE - Untarnished UI Patch](https://www.nexusmods.com/skyrimspecialedition/mods/140287) 1.1.3 by HotelKosmos | `7a16d51d684bb220f2e2c0ef9a89f4c20c06a0d975f456e5cc58b710b60f09c1` | see below |
| `untarnished-1.1.3/style2/LootMenuIE.swf` | same archive, `style2` | `a6136c916dda03c19e2204f9344bc1cf2d9083971afb6446c9c7125b3688c65b` | see below |
| `untarnished-1.1.3/style3/LootMenuIE.swf` | same archive, `style3` | `c27d5888603833be9b5276eaaf51a8245d822f303c01fa197cd64f9839cf7f68` | see below |
| `untarnished-1.1.3/style4/LootMenuIE.swf` | same archive, `style4` | `46a4bb35a6f3e227f4f832e07b0b61a67bdbb5db6b743e4e79670242b03266fb` | see below |
| `untarnished-1.1.3/style5/LootMenuIE.swf` | same archive, `style7` (the installer's Style 5; renamed to `style5` here) | `320090733a227f970ace70cd7e4c0340300b31e82e5c582ae1e93122fecc3450` | see below |

The 1.1.3 patch files are themselves modified QuickLoot IE 3.4.1 menus, so the GPL v3 applies to them as well. The
artwork is HotelKosmos's (based on AtomCrafty's reskin). The Nexus permissions for mod 140287 allow modification and
release of fixes without asking, and use of its assets; not for sale.
