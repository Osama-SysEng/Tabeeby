"""Defensive client-IP handling for trusted proxy deployments."""
from __future__ import annotations

import ipaddress
from collections.abc import Iterable


def parse_ip(value: str) -> ipaddress.IPv4Address | ipaddress.IPv6Address:
    try:
        return ipaddress.ip_address(value.strip())
    except ValueError as exc:
        raise ValueError("invalid IP address") from exc


def parse_networks(values: Iterable[str]) -> tuple[ipaddress.IPv4Network | ipaddress.IPv6Network, ...]:
    networks = []
    for value in values:
        try:
            networks.append(ipaddress.ip_network(value.strip(), strict=False))
        except ValueError as exc:
            raise ValueError(f"invalid trusted proxy network: {value}") from exc
    return tuple(networks)


def is_trusted_proxy(address: str, trusted_networks: Iterable[str]) -> bool:
    ip = parse_ip(address)
    return any(ip in network for network in parse_networks(trusted_networks))


def resolve_client_ip(peer_ip: str, forwarded_for: str | None, trusted_networks: Iterable[str]) -> str:
    """Return a client IP only when the immediate peer is a trusted proxy.

    Never trust X-Forwarded-For from an untrusted peer. When trusted, walk the
    chain from right to left and return the first address outside the proxy set.
    """
    peer = parse_ip(peer_ip)
    networks = parse_networks(trusted_networks)
    if not any(peer in network for network in networks) or not forwarded_for:
        return str(peer)
    chain = [parse_ip(part).compressed for part in forwarded_for.split(",") if part.strip()]
    chain.append(peer.compressed)
    for candidate in reversed(chain):
        ip = parse_ip(candidate)
        if not any(ip in network for network in networks):
            return ip.compressed
    return chain[0] if chain else peer.compressed


def reject_public_endpoint_target(host: str) -> None:
    """Reject SSRF-prone targets unless an explicit egress allow-list exists."""
    try:
        ip = parse_ip(host)
    except ValueError:
        return  # DNS names must be checked against an explicit hostname allow-list.
    if ip.is_loopback or ip.is_link_local or ip.is_multicast or ip.is_unspecified:
        raise ValueError("unsafe endpoint address")
